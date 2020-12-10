import graphene
from graphene_django import DjangoObjectType

from Cookbook.recipe.models import Recipe, IngredientsRecipe, Ingredient
from Cookbook.recipe.schemas.schemaIngredients import IngredientInput


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe

class Query(graphene.ObjectType):
    all_recipies = graphene.List(RecipeType)

    def resolve_all_recipies(self, info):
        return Recipe.objects.all()



class CreateRecipe(graphene.Mutation):
    id = graphene.Int()
    name =  graphene.String()
    description = graphene.String()
    class Input:
        ingredients = graphene.List(IngredientInput)

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        ingredients = graphene.List(IngredientInput)
    
    def mutate(self, info, name, description, ingredients):
        recipe = Recipe(name=name, description=description)
        recipe.save()

        for obj_ingredient in ingredients:
            ingredient = Ingredient.objects.filter(id=obj_ingredient.id).first()

            ingredientsRecipe = IngredientsRecipe(
                quantity= obj_ingredient.quantity, 
                recipe=recipe, 
                ingredient=ingredient)
            ingredientsRecipe.save()

        return CreateRecipe( 
            id = recipe.id,
            name = recipe.name,
            description = recipe.description,
            )

class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()