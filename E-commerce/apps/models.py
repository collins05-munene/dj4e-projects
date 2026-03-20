from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
id_validator = RegexValidator(
    regex = r'^\d{7,8}$',
    message = "Incorrect ID format"
)
phone_number_validator = RegexValidator(
    regex = r"^07\d{8}$",
    message = "Incorrect Number format"
)
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=30)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def profit(self):
        profit = self.selling_price - self.buying_price
        return profit

    def __str__(self):
        return self.name
    
class Admin(models.Model):
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_no = models.CharField(max_length=8, validators=[id_validator])
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10, validators=[phone_number_validator])
    created_at = models.DateTimeField(auto_now_add=True)

    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def __str__(self):
        return self.name
    
class Client(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10, validators=[phone_number_validator])
    id_no = models.CharField(max_length=8, validators=[id_validator])
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age
    
    def __str__(self):
        return self.name
