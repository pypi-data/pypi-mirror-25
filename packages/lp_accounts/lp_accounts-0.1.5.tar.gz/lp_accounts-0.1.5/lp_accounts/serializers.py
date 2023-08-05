from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from .models import User
from .validators import get_validator

import django.contrib.auth.password_validation as validators
import random
import string


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all())
    ])
    email = serializers.CharField(required=True, validators=[
        UniqueValidator(queryset=User.objects.all())
    ])
    type = serializers.ChoiceField(choices=User.TYPES)
    access_token = serializers.CharField(label=_('Access Token'), required=False)
    is_active = serializers.HiddenField(default=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'],
                                   first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        account_type = attrs.get('type')
        access_token = attrs.get('access_token')
        password = attrs.get('password')

        if account_type is not User.TYPE_DEFAULT and access_token:
            validator = get_validator(attrs['type'])
            if validator.validate(access_token):
                attrs['password'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
            else:
                raise serializers.ValidationError('access_token is not valid')
        elif account_type is not User.TYPE_DEFAULT:
            raise serializers.ValidationError('access_token is required')

        if account_type is User.TYPE_DEFAULT and password:
            validators.validate_password(password)
        elif account_type is User.TYPE_DEFAULT:
            raise serializers.ValidationError('password is required')

        return super(UserSerializer, self).validate(attrs)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(e)

        return value


class PasswordUpdateSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

    def validate_token(self, value):
        try:
            self.token = Token.objects.get(key=value)
            self.user = User.objects.get(id=self.token.user_id)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(e)

        return value


class AuthTokenSerializer(AuthTokenSerializer):
    account_type = serializers.ChoiceField(label=_('Account Type'), choices=User.TYPES)
    access_token = serializers.CharField(label=_('Access Token'), required=False)
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        account_type = attrs.get('account_type')
        access_token = attrs.get('access_token')

        if account_type is not User.TYPE_DEFAULT and access_token:
            try:
                validator = get_validator(account_type)
            except ValidationError as e:
                raise serializers.ValidationError(e)

            if validator.validate(access_token):
                try:
                    attrs['user'] = User.objects.get(username=username)
                except ObjectDoesNotExist as e:
                    raise serializers.ValidationError('user with username ' + username + ' not found')
            else:
                raise serializers.ValidationError('access_token is not valid')
        elif account_type is not User.TYPE_DEFAULT:
            raise serializers.ValidationError('username, account_type, and access_token are required for social login')

        if account_type is User.TYPE_DEFAULT:
            attrs = super(AuthTokenSerializer, self).validate(attrs)

        return attrs
