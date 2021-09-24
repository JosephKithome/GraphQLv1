import graphene
from graphene.types import interface
from graphene_django import DjangoObjectType,DjangoListField
from ingredients.models import (Category,Ingredient,PetModel)
from graphene import relay,ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from ingredients.serializers import CategorySerializer
from graphene_django.debug import DjangoDebug

class CategoryType(DjangoObjectType):
    class Meta:
        model =Category
        fields = ['id','name']
    extra_field = graphene.String()   
    #You can always add an extra_field this way
    def resolve_extra_field(self, info):
        return "hello!"     


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ['id','name','notes','category']
    

class PetType(DjangoObjectType):
    class Meta:
        model = PetModel
        fields = ("id", "kind",)
        convert_choices_to_enum = False


#<<<<<<<<<<<<<<<<<<<<< Update Mutation >>>>>>>>>>>>>>>>>>>>>#
class UpdatePetMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        kind =graphene.String(required=True)
    pet = graphene.Field(PetType)

     
    @classmethod
    def mutate(cls, root, info, kind, id):
        pet = PetModel.objects.get(pk=id)
        pet.kind = kind
        pet.save()
        # Notice we return an instance of this mutation
        return UpdatePetMutation(pet=pet) 
        
#<<<<<<<<<<<<<<<<<<<<< End Update Mutation >>>>>>>>>>>>>>>>>>>#      

#<<<<<<<<<<<<<<<<<<<<<<<<<<< Create Mutation >>>>>>>>>>>>>>>>>>#
class CreatePetMutation(graphene.Mutation):
    class Arguments:
        kind = graphene.String(required=True)
    pet = graphene.Field(PetType)

   
    @classmethod
    def mutate(cls,root,info,kind):
        pet = PetModel(kind=kind)   
        pet.save()
        return CreatePetMutation(pet=pet)  

#<<<<<<<<<<<<<<<<<<<<<<<<<<<End Create Mutation>>>>>>>>>>>>>>>

class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()

# We must define a query for our schema
class Query(graphene.ObjectType):
    person = graphene.Field(Person)
class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(root, info, name):
        person = Person(name=name)
        ok = True
        return CreatePerson(person=person, ok=ok)


class MyMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'
#<<<<<<<<<<<<<<<<Master Mutation >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
class Mutation(graphene.ObjectType):
    update_pet= UpdatePetMutation.Field()
    create_pet = CreatePetMutation.Field()
    create_person = CreatePerson.Field()


#<<<<<<<<<<<<<<<< End Master Mutation >>>>>>>>>>>>>>>>>>>>>>>>>>#   

class Query(graphene.ObjectType):
    all_categories = DjangoListField(CategoryType)
    category_by_name =graphene.Field(CategoryType,name=graphene.String(required=True))
    category_by_id = graphene.Field(CategoryType,id=graphene.String())

    all_ingredients = graphene.List(IngredientType)
    all_ingredientsAdvanced = DjangoListField(IngredientType)

    all_pets =graphene.List(PetType)
    debug = graphene.Field(DjangoDebug, name='_debug')


    def resolve_all_ingredients(root,info):
        return Ingredient.objects.select_related('category').all()

    def relove_all_ingredientsAdvanced(root,info):
        return Ingredient.objects.all()    

    def resolve_category_by_name(root,info,name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None
    def resolve_all_categories(root,info):
        return Category.objects.all()     

    def resolve_category_by_id(root,info,id):
        return Category.objects.get(pk=id)   


    def resolve_all_pets(root,info):
        return PetModel.objects.all()        

schema = graphene.Schema(query=Query,mutation=Mutation)   



# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class Query2(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)  
    debug = graphene.Field(DjangoDebug, name='_debug')    


schems = graphene.Schema(query=Query2)    
