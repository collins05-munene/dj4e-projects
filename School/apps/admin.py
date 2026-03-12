from django.contrib import admin
from .models import  Grade, Subject, Teacher, Student

# Register your models here.
admin.site.register(Grade)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)