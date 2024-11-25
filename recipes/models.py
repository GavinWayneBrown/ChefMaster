from django.db import models
from django.urls import reverse
from django.conf import settings
from sorl.thumbnail import ImageField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Recipe(models.Model, HitCountMixin):
    image = ImageField(upload_to="recipes/")
    title = models.CharField(max_length=100, default="Untitled Recipe")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )
    summary = models.CharField(max_length=500)
    prep_time = models.DurationField()
    cook_time = models.DurationField()
    total_time = models.DurationField()
    servings = models.IntegerField()
    categories = models.ManyToManyField("Category", blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field="object_pk", related_query_name="hit_count_generic"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})


class Instruction(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="instructions"
    )
    step = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Step for {self.recipe.title}: {self.step[:50]}"


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    item = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.item}"


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.recipe.title}"
