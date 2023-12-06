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

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_week = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    satisfied_requirements = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"UserProgress for {self.user.username}"

    class Meta:  # This should be nested inside the UserProgress class
        db_table = 'user_progress'

class Asana(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    important = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'asana'


class AsanasPerformed(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asana = models.ForeignKey(Asana, on_delete=models.CASCADE)


    def __str__(self):
        return f"Asana {self.asana.asana_id} is performed by user {self.user.user_id}"

    class Meta:
        db_table = 'asanas_performed'

class Step(models.Model):

    id = models.IntegerField(primary_key=True)
    technique = models.CharField(max_length=2000)
    order = models.IntegerField()

    class Meta:
        db_table = 'step'

class Course(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)

    class Meta:
        db_table = 'course'

class HasAsanas(models.Model):

    asana = models.ForeignKey(Asana, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = 'has_asana'

class HasSteps(models.Model):

    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    asana = models.ForeignKey(Asana, on_delete=models.CASCADE)

    class Meta:
        db_table = 'has_steps'

class Week(models.Model):

    id = models.IntegerField(primary_key=True)
    note = models.CharField(max_length=2000)

    class Meta:
        db_table = 'week'

class HasWeek(models.Model):

    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = 'has_week'

class ToDo(models.Model):

    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    asana = models.ForeignKey(Asana, on_delete=models.CASCADE)

    class Meta:
        db_table = 'to_do'

class Image(models.Model):

    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=150)

    class Meta:
        db_table = 'image'

