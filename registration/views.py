import environ

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from baby_backend.utils import (
    cognito_initiate_auth,
    get_user_data,
    cognito_global_sign_out,
)

from .forms import LoginForm

env = environ.Env()


def login_view(request):
    pass
