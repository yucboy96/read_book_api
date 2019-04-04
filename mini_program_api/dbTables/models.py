from django.db import models


# Create your models here.
class User(models.Model):
    openId = models.CharField(max_length=255)
    unionId = models.CharField(max_length=255)
    nickName = models.CharField(max_length=255)
    gender = models.CharField(default='0', max_length=1)
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    avatarUrl = models.TextField()
    session_key = models.TextField()

    def __str__(self):
        return self.openId
