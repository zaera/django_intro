from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.validators import validate_is_digits, validate_email


class User(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    email = models.EmailField(
        'email_address',
        blank=False,
        null=False,
        unique=True,
        # validators=(validate_email,),
    )

    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        default=None,
        validators=(validate_is_digits, ),
    )

    def save(self, *args, **kwargs):
        # print('before')
        # if not self.username:
        #     self.username = str(uuid.uuid4())
        # if self.phone:
        #     self.phone = ''.join(char for char in self.phone if char.isdigit())
        super().save(*args, **kwargs)
        # print('after')
