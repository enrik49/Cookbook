import graphene
from graphene_django import DjangoObjectType

from Cookbook.recipe.models import Ingredient

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class IngredientInput(graphene.InputObjectType):
    id = graphene.Int()
    quantity = graphene.Float()

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


class DeleteIngredient(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_ingredient = graphene.Int()
    
    def mutate(self, info, id_ingredient):
        ingredient = Ingredient.objects.get(id=id_ingredient)
        ingredient.delete()
        return DeleteIngredient(ok=True)

class Mutation(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()

    delete_ingredient = DeleteIngredient.Field()