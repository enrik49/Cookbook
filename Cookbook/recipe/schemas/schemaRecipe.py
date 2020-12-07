import graphene
from graphene_django import DjangoObjectType

from Cookbook.recipe.models import Recipe, IngredientsRecipe, Ingredient
from Cookbook.recipe.schemas.schemaIngredients import IngredientType


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

    class Arguments:
        name = graphene.String()
        description = graphene.String()
    
    def mutate(self, info, name, description):
        recipe = Recipe(name=name, description=description)
        recipe.save()

        return CreateRecipe( 
            id = recipe.id,
            name = recipe.name,
            description = recipe.description)

class CreateIngredientsRecipe(graphene.Mutation):
    id = graphene.Int()
    quantity = graphene.Float()
    recipe = graphene.Field(RecipeType)
    ingredient = graphene.Field(IngredientType)

    class Arguments:
        quantity = graphene.Float()
        id_recipe = graphene.Int()
        id_ingredient = graphene.Int()

    def mutate(self, info, quantity, id_recipe, id_ingredient):
        recipe = Recipe.objects.filter(id=id_recipe).first()
        ingredient = Ingredient.objects.filter(id=id_ingredient).first()

        ingredientsRecipe = IngredientsRecipe(quantity= quantity, recipe=recipe, ingredient=ingredient)
        ingredientsRecipe.save()

        return CreateIngredientsRecipe(
            id = ingredientsRecipe.id,
            quantity = ingredientsRecipe.quantity,
            recipe = ingredientsRecipe.recipe,
            ingredient = ingredientsRecipe.ingredient
        )

class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()
    create_ingredientsRecipe = CreateIngredientsRecipe.Field()