from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.users.models import User
from utils.codegen import generate_password
from utils.email.users import send_created_user_email


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'fullname']

    def save(self, tenant):
        user = User(email=self.validated_data['email'],
                    fullname=self.validated_data['fullname'],
                    tenant=tenant)

        password = generate_password()

        user.set_password(password)
        user.save()
        send_created_user_email(user, password)
        return user


class FakeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'fullname', 'password']

    def save(self, tenant):
        user = User(email=self.validated_data['email'],
                    fullname=self.validated_data['fullname'],
                    tenant=tenant)

        user.set_password(self.validated_data['password'])
        user.save()
        return user
