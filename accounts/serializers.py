from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """Serializer xử lý dữ liệu đầu vào cho API login."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Tên đăng nhập hoặc mật khẩu không đúng.')
        if not user.is_active:
            raise serializers.ValidationError('Tài khoản này đã bị vô hiệu hóa.')

        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer trả về thông tin user sau khi login thành công."""
    phone_number = serializers.CharField(source='account.phone_number', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer xử lý đăng ký tài khoản mới."""
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, max_length=10)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'phone_number']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Tên đăng nhập đã tồn tại.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email này đã được sử dụng.')
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Mật khẩu xác nhận không khớp.'})
        return data

    def create(self, validated_data):
        # Tách phone_number và password_confirm ra khỏi data trước khi tạo User
        phone_number = validated_data.pop('phone_number', None)
        validated_data.pop('password_confirm')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        # Tạo Account profile kèm phone_number
        Account.objects.create(user=user, phone_number=phone_number)

        return user
