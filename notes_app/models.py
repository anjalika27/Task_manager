from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
