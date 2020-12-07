import graphene
import Cookbook.recipe.schemas.schemaIngredients as sch_Ingredient
import Cookbook.recipe.schemas.schemaRecipe as sch_Recipe

class Query(sch_Ingredient.Query, sch_Recipe.Query, graphene.ObjectType):
    pass
class Mutation(sch_Ingredient.Mutation, sch_Recipe.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)