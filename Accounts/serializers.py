from rest_framework import serializers
from .models import User, Address
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'email',
                  'birth_day', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)

            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ForgetPasswordSerializer(serializers.Serializer):
    """
    Used for resetting password who forget their password via otp varification
    """
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'username',
                            'phone', 'created_at', 'is_active', 'is_admin',
                            'last_login', 'password')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'user',
            'province',
            'city',
            'address',
            'post_code'
        ]