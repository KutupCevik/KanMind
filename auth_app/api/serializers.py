from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']
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



    def validate(self, data):
        if data['password'] != data['repeated_pw']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_pw')
        user = User.objects.create_user(
            #Das User-Model von Django hat das Pflichtfeld "username"
            #https://docs.djangoproject.com/en/5.2/ref/contrib/auth/#user-model
            #Selbst wenn man sich per E-Mail einloggt, erwartet Django intern einen username
            username=validated_data['email'],   # Username intern = E-Mail
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['fullname']
        )
        Token.objects.create(user=user)
        return user