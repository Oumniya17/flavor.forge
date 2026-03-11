from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Rating, RecipeCard
from .models import Experiment

admin.site.register(Experiment)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Rating)
admin.site.register(RecipeCard)