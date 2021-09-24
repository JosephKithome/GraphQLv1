from django.db.models import fields
from rest_framework import serializers
from ingredients.models import(Category,Ingredient,CustomUser)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = ("__all__")