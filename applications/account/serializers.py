from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from applications.account.send_mail import send_confirmation_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate(self, atters):
        password = atters.get('password')
        password2 = atters.pop('password2')

        if password != password2:
            raise serializers.ValidationError('Password was not correct')
        return atters

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email(code, user.email)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not registered')
        return email

    def validate(self, atters):

        email = atters.get('email')
        password = atters.get('password')
        print(email, password)
        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                raise serializers.ValidationError('Not correct')

            atters['user'] = user
            return atters
