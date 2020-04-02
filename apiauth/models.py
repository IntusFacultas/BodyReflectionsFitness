from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
# Create your models here.


class Profile(models.Model):
    MALE = 1
    FEMALE = 2
    NOT_STATED = 3
    OTHER = 4
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (NOT_STATED, "Prefer not to state"),
        (OTHER, "Other")
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField("First Name", max_length=100)
    last_name = models.CharField("Last Name", max_length=150)
    age = models.IntegerField("Age")
    gender = models.IntegerField("Gender", choices=GENDER_CHOICES)
    date_joined = models.DateTimeField("Date Joined")
    email = models.EmailField("Email")

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_joined = timezone.now()
        self.user.email = self.email
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
