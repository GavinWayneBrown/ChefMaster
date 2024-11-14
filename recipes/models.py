from django.db import models


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100, default="Untitled Recipe")
    summary = models.CharField(max_length=500)
    prep_time = models.DurationField()
    cook_time = models.DurationField()
    total_time = models.DurationField()
    servings = models.IntegerField()
    ingredients = models.TextField()

    def __str__(self):
        return self.title


class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.TextField()

    def __str__(self):
        return f"{self.recipe.summary} - {self.step}"


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.recipe.summary} - {self.quantity} {self.item}"
