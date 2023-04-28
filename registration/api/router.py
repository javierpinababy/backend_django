from django.urls import path
from registration.api.views import RegisterView

urlpatterns = [path("auth/register/", RegisterView.as_view())]
