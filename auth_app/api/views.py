from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from auth_app.api.serializers import RegistrationSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "fullname": user.first_name,
                "email": user.email,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
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
    Nur für eingeloggte Benutzer zugänglich.
    '''

    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response({'detail': 'E-Mail-Adresse fehlt.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'E-Mail wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'id': user.id,
            'email': user.email,
            'fullname': user.first_name
        }
        return Response(data, status=status.HTTP_200_OK)