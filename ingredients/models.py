from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(blank=False,max_length=255,verbose_name="email")
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

class Category(models.Model):
    name =models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


from django.db import models
from graphene_django import DjangoObjectType

class PetModel(models.Model):
    kind = models.CharField(
        max_length=100,
        choices=(("cat", "Cat"), ("dog", "Dog"))
    )

    def __str__(self):
        return self.kind
