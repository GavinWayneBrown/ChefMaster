# Generated by Django 5.0.9 on 2024-11-19 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_recipe_author"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="instruction",
            options={"ordering": ["order"]},
        ),
        migrations.AddField(
            model_name="instruction",
            name="order",
            field=models.IntegerField(default=0),
        ),
    ]