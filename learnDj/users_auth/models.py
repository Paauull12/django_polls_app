from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
import uuid
from django.db import models
from datetime import date


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    def calculate_age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.is_superuser:
            age = self.calculate_age()

            user = CustomUser.objects.get(username=self.username)
            minor_group, created = Group.objects.get_or_create(name='Minor')
            adult_group, created = Group.objects.get_or_create(name='Adult')

            if age >= 18:
                user.groups.add(adult_group)
            else:
                user.groups.add(minor_group)

            super().save(*args, **kwargs)