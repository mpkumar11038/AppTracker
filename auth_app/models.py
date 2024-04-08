from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from auth_app.constants import JUDGE, STAFF,ADMIN,ESTAFF,USER
from auth_app.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication.

    This model extends the AbstractBaseUser and PermissionsMixin provided by
    Django to create a custom user model. It includes fields for email, staff
    status, active status, date of joining.
    """

    PROFILE_TYPE_CHOICES = [
        (JUDGE, JUDGE),
        (STAFF, STAFF),
        (ADMIN, ADMIN),
        (ESTAFF, ESTAFF),
        (USER, USER),

    ]

    email = models.EmailField(_("email address"), unique=True)
    profile = models.CharField(
        max_length = 2,
        choices = PROFILE_TYPE_CHOICES,
        default=USER,
        help_text = 'User profile type',
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def clean(self):
        # Ensure that the choice is one of the valid choices
        if self.profile not in dict(self.PROFILE_TYPE_CHOICES).keys():
            raise ValidationError({"profile": "Value too long for field 'profile' or invalid choice"})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
