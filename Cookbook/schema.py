import graphene
from graphene_django import DjangoObjectType

from Cookbook.recipe.models import Recipe, Ingredient

class RecipeType():
    class Meta:
        model = Recipe

class IngredientType():
    class Meta:
        model = Ingredient
    
class Query(graphene.ObjectType):
    info = graphene.String()

    def resolve_info(self, info , root):
        return "Mostrant info"

schema = graphene.Schema(query=Query)