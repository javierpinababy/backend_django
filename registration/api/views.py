from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from registration.api.serializers import UserRegisterSerializer, TestUserSerializer


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
            print(f"serializer: {serializer}")
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
