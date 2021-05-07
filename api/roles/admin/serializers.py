from rest_framework import serializers
from api.models import *
from django.contrib.auth import get_user_model


class CreateVehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name']


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(email=self.validated_data['email'],
                    username=self.validated_data['username'],
                    role=self.validated_data['role'])

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()
        return user
