from django.db import models
import datetime


# Create your models here.
# 用户名 密码 邮箱地址 性别 创建时间
class User(models.Model):
    gender = (('male', "男"), ('female', "女"),)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        # 为模型User增加了两个元数据‘ordering’和‘verbose_name_plural’，分别表示排序和复数名
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
