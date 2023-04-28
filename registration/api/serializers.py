from rest_framework import serializers
from registration.models import User


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
