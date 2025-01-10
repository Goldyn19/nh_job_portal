from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Job(models.Model):
    title = models.CharField(max_length=75)
    employer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.TextField(max_length=225)
    category = models.CharField(max_length=70)
    min_salary = models.IntegerField()
    max_salary = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company_url = models.URLField()

    def __str__(self):
        return self.title
# Create your models here.


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    seeker_id = models.ForeignKey()
    applied_at = models.DateTimeField(auto_now_add=True)
