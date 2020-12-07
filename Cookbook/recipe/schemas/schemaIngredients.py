import graphene
from graphene_django import DjangoObjectType

from Cookbook.recipe.models import Ingredient

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_ingredients(self, info):
        return Ingredient.objects.all()

class CreateIngredient(graphene.Mutation):
    id = graphene.Int()
    name =  graphene.String()

    class Arguments:
        name = graphene.String()
    
    def mutate(self, info, name):
        ingredient = Ingredient(name=name)
        ingredient.save()

        return CreateIngredient( 
            id = ingredient.id,
            name = ingredient.name)

class Mutation(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()