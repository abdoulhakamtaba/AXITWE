from django.db import models
from django.conf import settings
from shop.models import Item

# Create your models here.

class MyAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    item = models.ManyToManyField(Item)

    def __str__(self):
        return self.user.username
