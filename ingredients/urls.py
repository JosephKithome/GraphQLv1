from django.contrib import admin
from django.urls import path,include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from ingredients.schema import schems

urlpatterns = [
    path('graphql',csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('graphql2',csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schems)))
]
