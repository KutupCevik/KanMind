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

        user = authenticate(username=user_obj.username, password=password)  #warum muss ich authenticate sagen, dass es das Passwort prüft? Blöde funktion
        if not user:
            return Response({"detail": "Ungültige E-Mail oder Passwort."}, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "fullname": user.first_name,
            "email": user.email,
            "user_id": user.id
        }, status=200)


# class CustomLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({
#             "token": token.key,
#             "fullname": user.first_name,
#             "email": user.email,
#             "user_id": user.id
#         })


# class CustomLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         token = Token.objects.get(key=response.data['token'])
#         user = token.user
#         return Response({
#             'token': token.key,
#             'fullname': user.first_name,
#             'email': user.email,
#             'user_id': user.id
#         })