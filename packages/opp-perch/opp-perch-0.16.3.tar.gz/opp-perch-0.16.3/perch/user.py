# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
from __future__ import unicode_literals

import uuid
from datetime import datetime, timedelta
from enum import Enum

import couch
from dateutil import parser
from passlib.hash import pbkdf2_sha256
from tornado.gen import coroutine, Return
from tornado.options import options, define
from voluptuous import All, Extra, In, Length, Required, Schema

from . import views, exceptions, validators
from .model import Document, SubResource, State

__all__ = ['User', 'UserOrganisation', 'Token']

define('min_length_password', default=3)
define('max_length_password', default=128)
define('token_ttl', default=86400)


class User(Document):
    resource_type = 'user'
    view = views.users
    active_view = views.active_users
    db_name = 'registry'
    internal_fields = (Document.internal_fields +
                       ['password', 'verification_hash', 'pre_verified'])
    read_only_fields = ['created_by']

    default_state = State.approved
    editable_states = [State.approved]

    # State transitions for users overridden so that:
    # - Only valid states are approved and deactivated
    # - Once user is deactivated cannot be reactivated
    approval_state_transitions = {}

    state_transitions = {
        None: [State.approved.name],
        State.approved.name: [State.deactivated.name]
    }

    class roles(Enum):
        administrator = 'administrator'
        user = 'user'
        reseller = 'reseller'
        default = user

    @property
    def schema(cls):
        orgs_schema = Schema({
            Extra: {
                'state': validators.validate_state,
                'role': In([x.value for x in cls.roles]),
                'pre_verified': bool
            }
        }, required=True)

        password_length = Length(min=options.min_length_password,
                                 max=options.max_length_password)

        schema = Schema({
            '_id': unicode,
            '_rev': unicode,
            'doc_version': unicode,
            Required('type', default=cls.resource_type): cls.resource_type,
            Required('email'): validators.valid_email,
            Required('password'): All(unicode, password_length),
            Required('has_agreed_to_terms'): True,
            Required('organisations', default={}): orgs_schema,
            Required('state', default=User.default_state.name): validators.validate_user_state,
            Required('role', default=User.roles.default.value): In([x.value for x in User.roles]),
            'first_name': unicode,
            'last_name': unicode,
            'phone': unicode,
            'verification_hash': unicode,
            'pre_verified': bool, 
            'actor': unicode  # only used in fixtures, should it be removed?
        })

        return schema

    def clean(self):
        """Verified value is derived from whether user has a verification hash"""
        result = super(User, self).clean()
        result['verified'] = 'verification_hash' not in self._resource
        return result

    @coroutine
    def can_update(self, user, **kwargs):
        # Sys admin can update everything
        if user.is_admin():
            raise Return((True, set([])))

        # If user being updated can update everything apart from role
        if user.id == self.id:
            fields = ({'role'} & set(kwargs.keys()))
            if fields:
                raise Return((False, fields))
            else:
                raise Return((True, set([])))

        # Otherwise, cannot update
        raise Return((False, set([])))

    @coroutine
    def check_unique(self):
        """Check the user's email is unique"""
        emails = yield self.view.values(key=self.email)
        user_id = getattr(self, 'id', None)
        users = {x for x in emails if x != user_id and x}

        if users:
            raise exceptions.ValidationError(
                "User with email '{}' already exists".format(self.email))

    @classmethod
    @coroutine
    def create(cls, user, password, **kwargs):
        if not kwargs.get('pre_verified', False) or user is None or not user.is_reseller(): 
            kwargs['verification_hash'] = unicode(uuid.uuid4().hex)

        resource = cls(password=cls.hash_password(password), **kwargs)
        yield resource._save()

        raise Return(resource)

    @classmethod
    @coroutine
    def create_admin(cls, email, password, **kwargs):
        """
        Create an approved 'global' administrator

        :param email: the user's email address
        :param password: the user's plain text password
        :returns: a User
        """
        data = {
            'email': email,
            'password': cls.hash_password(password),
            'has_agreed_to_terms': True,
            'state': State.approved,
            'role': cls.roles.administrator.value,
            'organisations': {}
        }
        data.update(**kwargs)

        user = cls(**data)
        yield user._save()

        raise Return(user)

    @staticmethod
    def hash_password(plain_text):
        """Hash a plain text password"""
        # NOTE: despite the name this is a one-way hash not a reversible cypher
        hashed = pbkdf2_sha256.encrypt(plain_text, rounds=8000, salt_size=10)
        return unicode(hashed)

    def verify_password(self, password):
        """Verify the password matches the hash"""
        return pbkdf2_sha256.verify(password, self.password)

    @coroutine
    def change_password(self, previous, new_password):
        """
        Change the user's password and save to the database

        :param previous: plain text previous password
        :param new_password: plain text new password
        :raises: ValidationError
        """
        if not self.verify_password(previous):
            raise exceptions.Unauthorized('Incorrect password')

        if len(new_password) < options.min_length_password:
            msg = ('Passwords must be at least {} characters'
                   .format(options.min_length_password))
            raise exceptions.ValidationError(msg)

        if len(new_password) > options.max_length_password:
            msg = ('Passwords must be at no more than {} characters'
                   .format(options.max_length_password))
            raise exceptions.ValidationError(msg)

        self.password = self.hash_password(new_password)
        yield self._save()

    @classmethod
    @coroutine
    def login(cls, email, password):
        """
        Log in a user

        :param email: the user's email address
        :param password: the user's password
        :returns: (User, token)
        :raises: SocketError, CouchException
        """
        try:
            doc = yield cls.view.first(key=email, include_docs=True)
        except couch.NotFound:
            raise exceptions.Unauthorized('Unknown email address')

        user = cls(**doc['doc'])

        verified = user.verify_password(password)
        if not verified:
            raise exceptions.Unauthorized('Invalid password')

        token = yield Token.create(user)
        raise Return((user, token.id))

    @classmethod
    @coroutine
    def verify(cls, user_id, verification_hash):
        """
        Verify a user using the verification hash

        The verification hash is removed from the user once verified

        :param user_id: the user ID
        :param verification_hash: the verification hash
        :returns: a User instance
        """
        user = yield cls.get(user_id)

        # If user does not have verification hash then this means they have already been verified
        if 'verification_hash' not in user._resource:
            raise Return(user)

        if user.verification_hash != verification_hash:
            raise exceptions.ValidationError('Invalid verification hash')

        del user.verification_hash
        yield user._save()

        raise Return(user)

    def is_admin(self):
        """Is the user a system administrator"""
        return self.role == self.roles.administrator.value and self.state == State.approved

    def is_reseller(self):
        """is the user a reseller"""
        return self.role == self.roles.reseller.value and self.state == State.approved

    def is_org_admin(self, organisation_id):
        """Is the user authorized to administrate the organisation"""
        return (self._has_role(organisation_id, self.roles.administrator) or
                self.is_admin())

    def is_user(self, organisation_id):
        """Is the user valid and approved in this organisation"""
        return (self._has_role(organisation_id, self.roles.user) or
                self.is_org_admin(organisation_id))

    def _has_role(self, organisation_id, role):
        """Check the user's role for the organisation"""
        if organisation_id is None:
            return False

        try:
            org = self.organisations.get(organisation_id, {})
            user_role = org.get('role')
            state = org.get('state')
        except AttributeError:
            return False

        return user_role == role.value and state == State.approved.name

    @classmethod
    @coroutine
    def remove_organisation_from_all(cls, organisation_id):
        """Remove an organisation from all users"""
        users = yield views.organisation_members.get(key=organisation_id,
                                                     include_docs=True)
        users = [x['doc'] for x in users['rows']]
        for user in users:
            user['organisations'][organisation_id]['state'] = State.deactivated.name

        db = cls.db_client()
        yield db.save_docs(users)


class Token(Document):
    resource_type = 'token'
    db_name = 'token'
    read_only_fields = ['token_ttl', 'user_id']

    @classmethod
    @coroutine
    def create(cls, user):
        token = cls(user_id=user.id)
        if 'token_ttl' not in token._resource:
            ttl = (datetime.utcnow() + timedelta(seconds=options.token_ttl))

        token.token_ttl = ttl.isoformat()
        yield token._save()

        raise Return(token)

    @property
    def ttl(self):
        return parser.parse(self.token_ttl)

    @classmethod
    @coroutine
    def valid(cls, token, **kwargs):
        """
        Check if a token exists and has not expired

        :param token: the token
        :return: bool
        """
        try:
            token = yield cls.get(token)
        except couch.NotFound:
            raise Return(False)

        raise Return(token.ttl >= datetime.utcnow())


class UserOrganisation(SubResource):
    resource_type = 'user_organisation'
    parent_resource = User
    parent_key = 'organisations'
    view = views.user_organisations_resource
    active_view = views.active_user_organisations_resource
    internal_fields = ['id', 'user_id', 'pre_verified']
    editable_states = [State.approved]

    schema = Schema({
        'id': unicode,
        'user_id': unicode,
        Required('state', default=SubResource.default_state.name): validators.validate_state,
        Required('role', default=User.roles.default.value): In([x.value for x in User.roles]),
        'pre_verified': bool
    }, )

    @property
    def organisation_id(self):
        return self.id

    @coroutine
    def can_approve(self, user, **data):
        """
        Only org admins can approve joining an organisation
        :param user: a User
        :param data: data that the user wants to update
        """
        is_org_admin = user.is_org_admin(self.organisation_id)

        is_reseller_preverifying = user.is_reseller() and data.get('pre_verified', False)

        raise Return(is_org_admin or is_reseller_preverifying)

    @coroutine
    def can_update(self, user, **kwargs):
        # Can only update if org admin or user being updated
        if not (user.id == self.user_id or user.is_org_admin(self.organisation_id)):
            raise Return((False, set([])))

        if 'role' in kwargs:
            if not user.is_org_admin(self.organisation_id):
                raise Return((False, {'role'}))

        raise Return((True, set([])))
