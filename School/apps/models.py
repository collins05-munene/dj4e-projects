from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=13)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    subject = models.ManyToManyField(Subject)

    def __str__ (self):
        return self.name

class Grade(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=6)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    

    
class Student(models.Model):
    name = models.CharField(max_length=30)
    subjects = models.ManyToManyField(Subject)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True) 
    adm = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.adm}"

