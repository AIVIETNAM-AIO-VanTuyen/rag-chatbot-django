from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'accounts'

urlpatterns = [
    # POST /api/accounts/register/ - Đăng ký tài khoản mới
    path('register/', views.RegisterView.as_view(), name='register'),

    # POST /api/accounts/login/ - Đăng nhập, nhận JWT token
    path('login/', views.LoginView.as_view(), name='login'),

    # POST /api/accounts/logout/ - Đăng xuất, blacklist refresh token
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # POST /api/accounts/token/refresh/ - Làm mới access token bằng refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
