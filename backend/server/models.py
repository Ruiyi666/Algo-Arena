from django.db import models

# Create your models here.


class Strategy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Game(models.Model):
    name = models.CharField(max_length=100)
