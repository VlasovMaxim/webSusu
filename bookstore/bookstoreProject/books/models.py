from django.db import models
from django import forms
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField("Название", max_length=255)
    author = models.CharField("Автор", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.TextField()
    name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[("user", "User"), ("admin", "Admin")], default="user")

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return self.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "name"]