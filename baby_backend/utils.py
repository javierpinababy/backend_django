import environ
import base64
import requests
import boto3
import json
import os
import sys, hmac, hashlib
import jwt
from jwt import PyJWKClient
from django.http import HttpResponseRedirect

env = environ.Env()


def cognito_initiate_auth(username: str, password: str):
    client_id = env("AWS_COGNITO_CLIENT_ID")
    client_secret = env("AWS_COGNITO_CLIENT_SECRET")
    region = env("AWS_REGION")
    auth_flow = env("AWS_COGNITO_AUTHFLOW")

    message = bytes(username + client_id, "utf-8")
    client_secret = bytes(client_secret, "utf-8")
    secret_hash = base64.b64encode(
        hmac.new(client_secret, message, digestmod=hashlib.sha256).digest()
    ).decode()

    client = boto3.client("cognito-idp", region_name=region)
    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow=auth_flow,
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
            "SECRET_HASH": secret_hash,
        },
    )
    return response


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
