import graphene
from graphene_django import DjangoObjectType

from Cookbook.recipe.models import Recipe, IngredientsRecipe, Ingredient
from Cookbook.recipe.schemas.schemaIngredients import IngredientInput


class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe

class IngredientsRecipeType(DjangoObjectType):
    class Meta:
        model = IngredientsRecipe

#------------------------------------Query's

class Query(graphene.ObjectType):
    all_recipies = graphene.List(RecipeType)

    def resolve_all_recipies(self, info):
        return Recipe.objects.all()

#------------------------------------Mutation's

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
            ingredient = Ingredient.objects.get(id=obj_ingredient.id)

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

class DeleteRecipe(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_recipe = graphene.Int()
    
    def mutate(self, info, id_recipe):
        recipe = Recipe.objects.get(id=id_recipe)
        recipe.delete()
        return DeleteRecipe(ok=True)

class DeleteIngredientRecipe(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_ingredient_recipe = graphene.Int()
    
    def mutate(self, info, id_ingredient_recipe):
        ing_recipe = IngredientsRecipe.objects.get(id=id_ingredient_recipe)
        ing_recipe.delete()
        return DeleteIngredientRecipe(ok=True)

        
class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()

    delete_recipe = DeleteRecipe.Field()
    delete_recipe_ingredient = DeleteIngredientRecipe.Field()