from rest_framework import serializers
from registration.models import User, Profile


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]

    def create(self, validated_date):
        password = validated_date.pop("password", None)
        instance = self.Meta.model(**validated_date)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "avatar",
            "bio",
            "link",
        ]
        # mirar bien y usar profile


class TestUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField()

    def validate_username(self, value):
        if value == "":
            raise serializers.ValidationError("Tiene que indicar un nombre de usuario")
        print(value)
        return value

    def validate(self, data):
        return data
