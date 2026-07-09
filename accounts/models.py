from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    email = models.EmailField(unique=True, blank=False, max_length=254, verbose_name="Email")
    phone_number = models.CharField(max_length=10, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.username


class ChatbotRole(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên vai trò")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã vai trò")
    avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name="Đường dẫn ảnh đại diện")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả ngắn")
    system_prompt = models.TextField(verbose_name="Prompt hệ thống")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chatbot_roles'
        verbose_name = 'Vai trò Chatbot'
        verbose_name_plural = 'Danh sách Vai trò Chatbot'

    def __str__(self):
        return self.name


