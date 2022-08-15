from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, \
    ForgotPasswordSerializer, ForgotPasswordCompleteSerializer
from applications.notifications.models import Contact

User = get_user_model()


class RegisterApiView(APIView):

    def post(self, request):
        data = request.data
        serializers = RegisterSerializer(data=data)

        if serializers.is_valid(raise_exception=True):
            serializers.save()
            message = f'Вы зарегестрированны, вам отправленно письмо активации.'

            return Response(message, status=201)


class LoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer


class ActivationView(APIView):

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.activation_code = ' '
            user.is_active = True
            user.save()
            contact, _ = Contact.objects.get_or_create(email=user.email)
            contact.save()
            return Response('всё удачно прошло', status=200)
        except User.DoesNotExist:
            return Response('неверный код', status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data,
                                               context={'request': request})

        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Пароль успешно обнавлен!')


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам отправлено письмо для восстановления пароля')


class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Пароль успешно обновлен!')
