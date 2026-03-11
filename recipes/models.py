from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# INGREDIENT MODEL
class Ingredient(models.Model):

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    calories = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.name


# RECIPE MODEL
class Recipe(models.Model):

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    instructions = models.TextField()

    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    def __str__(self):
        return self.title


# RECIPE INGREDIENT MODEL
class RecipeIngredient(models.Model):

    UNIT_CHOICES = [
        ('g', 'grams'),
        ('kg', 'kilograms'),
        ('ml', 'milliliters'),
        ('l', 'liters'),
        ('tsp', 'teaspoon'),
        ('tbsp', 'tablespoon'),
        ('cup', 'cup'),
        ('unit', 'unit')
    ]

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )

    quantity = models.FloatField(
        validators=[MinValueValidator(0.01)]
    )

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES
    )

    class Meta:
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient} in {self.recipe}"


# RATING MODEL
class Rating(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['recipe', 'user']

    def __str__(self):
        return f"{self.recipe} - {self.score}"


# RECIPE CARD MODEL (FAVORITES / NOTES)
class RecipeCard(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    personal_notes = models.TextField(blank=True)

    favorite = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.recipe}"


# EXPERIMENT MODEL
class Experiment(models.Model):

    original_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='experiments'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# EXPERIMENT VOTE MODEL
class ExperimentVote(models.Model):

    experiment = models.ForeignKey(
        Experiment,
        on_delete=models.CASCADE,
        related_name='experiment_votes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['experiment', 'user']

    def __str__(self):
        return f"{self.user} voted for {self.experiment}"