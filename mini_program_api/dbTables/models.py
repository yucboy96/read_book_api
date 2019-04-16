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
    language = models.CharField(max_length=32)
    avatarUrl = models.TextField()
    session_key = models.TextField()

    def __str__(self):
        return self.openId


class Variable(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    value = models.TextField()
    lifeTime = models.CharField(max_length=64)
    lastModify = models.DateTimeField(auto_now_add=True)


class Bookshelf(models.Model):
    webUrl = models.TextField()
    imgUrl = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    sessionId = models.IntegerField()
    writer = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    info = models.TextField()
    lastRead = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("imgUrl", "sessionId"),)
