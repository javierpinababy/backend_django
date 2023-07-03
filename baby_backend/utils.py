import environ
import base64
import requests
import boto3
import botocore
import json
import os
import sys, hmac, hashlib
import jwt
from jwt import PyJWKClient
from django.http import HttpResponseRedirect

env = environ.Env()


def get_secret_hash(username: str, client_secret: str, client_id: str):
    # A keyed-hash message authentication code (HMAC) calculated using
    # the secret key of a user pool client and username plus the client
    # ID in the message.
    message = username + client_id
    dig = hmac.new(
        client_secret, msg=message.encode("UTF-8"), digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()


def cognito_initiate_auth(username: str, password: str):
    client_id = env("AWS_COGNITO_CLIENT_ID")
    client_secret = env("AWS_COGNITO_CLIENT_SECRET")
    region = env("AWS_REGION")
    auth_flow = env("AWS_COGNITO_AUTHFLOW")

    print(f"client_id: {client_id}")
    print(f"client_secret: {client_secret}")
    print(f"region: {region}")
    print(f"auth_flow: {auth_flow}")

    message = bytes(username + client_id, "utf-8")
    client_secret = bytes(client_secret, "utf-8")
    """secret_hash = base64.b64encode(
        hmac.new(client_secret, message, digestmod=hashlib.sha256).digest()
    ).decode()"""
    secret_hash = get_secret_hash(
        username=username, client_secret=client_secret, client_id=client_id
    )
    print(f"client_secret: {client_secret}")
    print(f"secret_hash: {secret_hash}")

    try:
        client = boto3.client("cognito-idp", region_name=region)
        return client.initiate_auth(
            ClientId=client_id,
            AuthFlow=auth_flow,
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secret_hash,
            },
        )
    except botocore.exceptions.ClientError as e:
        return e.response


def get_user_data(token: str):
    REGION = env("AWS_REGION")
    USER_POOL_ID = env("AWS_COGNITO_USER_POOL_ID")
    ALG = "RS256"
    URL = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"

    jwks_client = PyJWKClient(URL)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    user_data = jwt.decode(
        token, signing_key.key, audience=env("AWS_COGNITO_CLIENT_ID"), algorithms=[ALG]
    )

    return user_data


def cognito_global_sign_out():
    domain = env("AWS_COGNITO_DOMAIN")
    scope = env("AWS_COGNITO_SCOPE")
    client_id = env("AWS_COGNITO_CLIENT_ID")
    client_secret = env("AWS_COGNITO_CLIENT_SECRET")
    redirect_uri = env("AWS_COGNITO_REDIRECT_URI")

    url = f"{domain}logout?client_id={client_id}&logout_uri={redirect_uri}"

    return url


def login_cognito_chatgpt(username: str, password: str):
    region = env("AWS_REGION")
    client = boto3.client("cognito-idp", region_name=region)

    client_id = env("AWS_COGNITO_CLIENT_ID")
    client_secret = env("AWS_COGNITO_CLIENT_SECRET")
    username = username
    password = password

    # Calculate the SecretHash
    message = username + client_id
    key = client_secret.encode("utf-8")
    msg = message.encode("utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).digest()
    secret_hash = base64.b64encode(digest).decode()

    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=client_id,
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
            # "SECRET_HASH": secret_hash,
        },
    )

    print(f"response: {response}")

    if response.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
        session = response.get("session")
        challenge_name = "NEW_PASSWORD_REQUIRED"
        challenge_responses = {"USERNAME": "javier", "NEW_PASSWORD": "2Lechugas!"}

        response = client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName=challenge_name,
            ChallengeResponses=challenge_responses,
            Session=session,
        )

    print(f"response: {response}")
