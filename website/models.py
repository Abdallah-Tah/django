from django.db import models
from django.contrib.auth.models import User


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class UserProgress(models.Model):

    id = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id',primary_key=True)
    #id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id',primary_key=True)
    current_week = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    satisfied_requirements = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"UserProgress for {self.user.username}"

    class Meta:  # This should be nested inside the UserProgress class
        db_table = 'user_progress'
