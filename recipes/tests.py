from django.test import TestCase
from .models import Recipe, Instruction, Ingredient
from datetime import timedelta

class RecipeModelTest(TestCase):

    def setUp(self):
        # Create sample data for testing
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            summary="This is a test recipe",
            prep_time=timedelta(minutes=10),
            cook_time=timedelta(minutes=20),
            total_time=timedelta(minutes=30),
            servings=4
        )
        self.ingredient1 = Ingredient.objects.create(
            recipe=self.recipe,
            item="Test Ingredient 1",
            quantity="1 cup"
        )
        self.ingredient2 = Ingredient.objects.create(
            recipe=self.recipe,
            item="Test Ingredient 2",
            quantity="2 cups"
        )
        self.instruction1 = Instruction.objects.create(
            recipe=self.recipe,
            step="Test instruction 1"
        )
        self.instruction2 = Instruction.objects.create(
            recipe=self.recipe,
            step="Test instruction 2"
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, "Test Recipe")
        self.assertEqual(self.recipe.summary, "This is a test recipe")
        self.assertEqual(self.recipe.prep_time, timedelta(minutes=10))
        self.assertEqual(self.recipe.cook_time, timedelta(minutes=20))
        self.assertEqual(self.recipe.total_time, timedelta(minutes=30))
        self.assertEqual(self.recipe.servings, 4)

    def test_ingredient_creation(self):
        ingredients = Ingredient.objects.filter(recipe=self.recipe)
        self.assertEqual(ingredients.count(), 2)
        self.assertEqual(ingredients[0].item, "Test Ingredient 1")
        self.assertEqual(ingredients[0].quantity, "1 cup")
        self.assertEqual(ingredients[1].item, "Test Ingredient 2")
        self.assertEqual(ingredients[1].quantity, "2 cups")

    def test_instruction_creation(self):
        instructions = Instruction.objects.filter(recipe=self.recipe)
        self.assertEqual(instructions.count(), 2)
        self.assertEqual(instructions[0].step, "Test instruction 1")
        self.assertEqual(instructions[1].step, "Test instruction 2")