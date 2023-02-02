from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_projects")
    # total = models.DecimalField(decimal_places = 2, max_digits = 10)
    liked_by = models.ManyToManyField(User, related_name="liked_projects")

    @property
    def total(self):
        return self.pledges.aggregate(sum=models.Sum("pledge_amount"))["sum"]


class Pledge(models.Model):
    pledge_amount = models.DecimalField(decimal_places=2, max_digits=10)
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="pledges")
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supporter_pledges")
