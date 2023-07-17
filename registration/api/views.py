from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from registration.api.serializers import UserRegisterSerializer, TestUserSerializer
from baby_backend.utils import (
    cognito_initiate_auth,
    cognito_global_sign_out,
    get_user_data,
    login_cognito_chatgpt,
)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def get(self, request):
        serializer = TestUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # serializer.save()

            username = serializer.data.get("username")
            password = serializer.data.get("password")

            print(f"username: {username}")
            print(f"password: {password}")

            response = login_cognito_chatgpt(username=username, password=password)

            print(f"response: {response}")

            request.session["AuthenticationResult"] = response.get(
                "AuthenticationResult"
            )

            id_token = response.get("AuthenticationResult").get("IdToken")
            user_data = get_user_data(id_token)

            request.session["user_data"] = user_data
            request.session["groups"] = user_data["cognito:groups"]

            response["user_data"] = user_data

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = TestUserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            print(f"serializer: {serializer}")
            # serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
