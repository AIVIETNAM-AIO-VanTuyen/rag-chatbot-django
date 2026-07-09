from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, UserProfileSerializer, RegisterSerializer


def get_tokens_for_user(user):
    """Tạo JWT access và refresh token cho user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    """
    API Login - Xác thực người dùng và trả về JWT token.

    POST /api/accounts/login/
    Body: { "email": "...", "password": "..." }

    Response (200):
    {
        "message": "Đăng nhập thành công.",
        "user": { id, username, email, first_name, last_name, phone_number },
        "tokens": { "access": "...", "refresh": "..." }
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            print(1111)
            return Response(
                {
                    'message': 'Đăng nhập thất bại.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        user_data = UserProfileSerializer(user).data

        return Response(
            {
                'message': 'Đăng nhập thành công.',
                'user': user_data,
                'tokens': tokens,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    API Logout - Vô hiệu hóa refresh token.

    POST /api/accounts/logout/
    Header: Authorization: Bearer <access_token>
    Body: { "refresh": "<refresh_token>" }
    """

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'message': 'Refresh token là bắt buộc.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {'message': 'Token không hợp lệ hoặc đã hết hạn.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': 'Đăng xuất thành công.'},
            status=status.HTTP_200_OK,
        )


class RegisterView(APIView):
    """
    API Đăng ký tài khoản mới.

    POST /api/accounts/register/
    Body:
    {
        "username": "...",
        "email": "...",
        "password": "...",
        "password_confirm": "...",
        "first_name": "...",   (tuỳ chọn)
        "last_name": "...",    (tuỳ chọn)
        "phone_number": "..."  (tuỳ chọn)
    }

    Response (201):
    {
        "message": "Đăng ký thành công.",
        "user": { id, username, email, first_name, last_name, phone_number },
        "tokens": { "access": "...", "refresh": "..." }
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Đăng ký thất bại.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        tokens = get_tokens_for_user(user)
        user_data = UserProfileSerializer(user).data

        return Response(
            {
                'message': 'Đăng ký thành công.',
                'user': user_data,
                'tokens': tokens,
            },
            status=status.HTTP_201_CREATED,
        )
