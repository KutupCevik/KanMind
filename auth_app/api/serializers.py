from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}
        #extra_kwargs erlaubt, Verhalten einzelner Felder anzupassen
        #Passwort nur eingeben, nie zurückgeben

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user