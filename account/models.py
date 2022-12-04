from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Acc_Pass_Change(models.Model):
    username_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=200, default='', null=True)
    secretInt = models.BigIntegerField(default=238123, null=True) # default is a random number for security purposes
    newPassword = models.CharField(max_length=50, default='', null=True)

    def __str__(self):
        return str(self.username_id)

    class Meta:
        verbose_name_plural = "Password_Change_Requests"
