# Third-party
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate
import re

# Lokale Module
from auth_app.api.serializers import RegistrationSerializer


class RegistrationView(APIView):
    '''
    POST /registration/
    '''
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except IntegrityError:
                return Response(
                    {"detail": "Ein Benutzer mit dieser E-Mail-Adresse existiert bereits."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": user.first_name,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    '''
    POST /login/
    '''
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Ungültige E-Mail oder Passwort."}, status=400)

        user = authenticate(username=user_obj.username, password=password)
        if not user:
            return Response({"detail": "Ungültige E-Mail oder Passwort."}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "fullname": user.first_name,
            "email": user.email,
            "user_id": user.id
        }, status=200)


class EmailCheckView(APIView):
    '''
    GET /api/email-check/
    Prüft, ob eine E-Mail im System existiert.
    '''
    def get(self, request):
        email = request.query_params.get('email')

        # 400 – keine oder ungültige E-Mail
        if not email:
            return Response(
                {'detail': 'E-Mail-Adresse fehlt oder hat ein falsches Format.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Formatprüfung per Regex
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return Response(
                {'detail': 'E-Mail-Adresse fehlt oder hat ein falsches Format.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 404 – Benutzer nicht gefunden
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'E-Mail wurde nicht gefunden.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 200 – Erfolg
        data = {
            'id': user.id,
            'email': user.email,
            'fullname': user.first_name
        }
        return Response(data, status=status.HTTP_200_OK)