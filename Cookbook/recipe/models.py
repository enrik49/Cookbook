from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientsRecipe')

    def __str__(self):
        return self.name

class IngredientsRecipe(models.Model):
    quantity = models.FloatField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)