from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.JSONField(default=dict)

    def __str__(self):
        return f"Cart for {self.user.username}"
    