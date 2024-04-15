from django.db import models

from auth_app.models import User
from applications.constants import (
    PENDING,
    APPROVED,
    REJECTED
)

class Category(models.Model):
    name = models.CharField(max_length=100)

class Application(models.Model):
    status_choices = [
        (PENDING, PENDING),
        (APPROVED, APPROVED),
        (REJECTED, REJECTED)
    ]

    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default=PENDING)

    class Meta:
        unique_together = ('applicant', 'category')
