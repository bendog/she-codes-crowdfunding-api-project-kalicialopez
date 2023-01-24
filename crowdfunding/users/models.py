from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    profile_picture = models.URLField(blank=True)
    bio = models.TextField(blank=True, null=True)
    country_of_residence = models.CharField(max_length=200, blank=False)


    def __str__(self):
        return self.username
    


# Create your models here.
