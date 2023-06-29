from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
"""
user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
"""
class FinancialInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    credit_card_number = models.CharField(max_length=16)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return self.user.username

class ScanResult(models.Model):
    scan_id = models.AutoField(primary_key=True)
    result = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan ID: {self.scan_id}, Result: {self.result}"

 