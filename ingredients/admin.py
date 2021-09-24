from django.contrib import admin
from ingredients.models import (Category,Ingredient,PetModel)

# Register your models here.


admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(PetModel)