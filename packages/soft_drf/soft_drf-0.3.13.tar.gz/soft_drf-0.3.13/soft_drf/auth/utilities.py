# -*- coding: utf-8 -*-
import uuid
from calendar import timegm
from datetime import datetime

from django.contrib.auth import get_user_model

from jwt import decode, encode

from rest_framework_jwt.settings import api_settings


def jwt_get_secret_key(payload=None):
    """
    For enchanced security you may use secret key on user itself.
    This way you have an option to logout only this user if:
        - token is compromised
        - password is changed
        - etc.
    """
    User = get_user_model()  # noqa
    if api_settings.JWT_GET_USER_SECRET_KEY:
        user = User.objects.get(pk=payload.get('user_id'))
        key = str(api_settings.JWT_GET_USER_SECRET_KEY(user))
        return key

    return api_settings.JWT_SECRET_KEY


def jwt_payload_handler(user):
    username_field = 'email'
    username = user.email

    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def jwt_get_user_id_from_payload_handler(payload):
    return payload.get('user_id')


def jwt_get_username_from_payload_handler(payload):
    return payload.get('username')


def jwt_encode_handler(payload):
    key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)
    return encode(
        payload,
        key,
        api_settings.JWT_ALGORITHM
    ).decode('utf-8')


def jwt_decode_handler(token):
    """
    Decode token for user
    """
    options = {
        'verify_exp': False,
    }
    unverified_payload = decode(token, None, False)
    secret_key = jwt_get_secret_key(unverified_payload)

    return decode(
        token,
        api_settings.JWT_PUBLIC_KEY or secret_key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM]
    )


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token
    }


def create_token(user):
    """
    Create token.
    """
    payload = jwt_payload_handler(user)
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    # Return values
    token = jwt_encode_handler(payload)
    return token
