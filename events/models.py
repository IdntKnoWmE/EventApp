from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractUser

from events.helper import validate_interval


class EventUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.email_validator(self.email)
        try:
            EventUser.obects.get(email=self.email)
        except ObjectDoesNotExist:
            raise Exception("Email already exist")

    @classmethod
    def email_validator(cls, email):
        """
        Normalize the email address making it lowercase.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name.lower() + "@" + domain_part.lower()
        return email


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.title


class UserInterest(models.Model):
    user = models.ForeignKey(EventUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} interested in {self.event.title}"


class EventRating(models.Model):
    user = models.ForeignKey(EventUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[validate_interval])

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} rated {self.event.title} - {self.rating}"
