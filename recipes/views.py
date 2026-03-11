from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib import messages

from .models import Recipe, Experiment, ExperimentVote, RecipeIngredient
from .forms import (
    RecipeForm,
    ExperimentForm,
    RecipeIngredientForm,
    IngredientForm
)

from django.contrib.auth.forms import UserCreationForm


# ===============================
# LISTA DE RECETAS
# ===============================
def recipe_list(request):

    recipes = Recipe.objects.all().order_by('-created_at')

    search = request.GET.get('search')
    difficulty = request.GET.get('difficulty')
    order = request.GET.get('order')

    if search:
        recipes = recipes.filter(title__icontains=search)

    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    if order:
        recipes = recipes.order_by(order)

    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_list.html', {
        'page_obj': page_obj
    })


# ===============================
# DETALLE DE RECETA
# ===============================
def recipe_detail(request, pk):

    recipe = get_object_or_404(Recipe, pk=pk)

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe
    })


# ===============================
# CREAR RECETA
# ===============================
@login_required
def recipe_create(request):

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()

            return redirect('recipe_detail', pk=recipe.pk)

    else:
        form = RecipeForm()

    return render(request, 'recipes/recipe_form.html', {
        'form': form
    })


# ===============================
# EDITAR RECETA
# ===============================
@login_required
def recipe_edit(request, pk):

    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)

    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_form.html', {
        'form': form
    })


# ===============================
# ELIMINAR RECETA
# ===============================
@login_required
def recipe_delete(request, pk):

    recipe = get_object_or_404(Recipe, pk=pk)

    if request.user != recipe.created_by:
        return redirect('recipe_detail', pk=recipe.pk)

    if request.method == "POST":
        recipe.delete()
        return redirect('recipe_list')

    return render(request, 'recipes/recipe_confirm_delete.html', {
        'recipe': recipe
    })


# ===============================
# CREAR EXPERIMENT
# ===============================
@login_required
def experiment_create(request, recipe_pk):

    recipe = get_object_or_404(Recipe, pk=recipe_pk)

    if request.method == 'POST':
        form = ExperimentForm(request.POST)

        if form.is_valid():
            experiment = form.save(commit=False)
            experiment.original_recipe = recipe
            experiment.created_by = request.user
            experiment.save()

            return redirect('recipe_detail', pk=recipe.pk)

    else:
        form = ExperimentForm()

    return render(request, 'recipes/experiment_form.html', {
        'form': form,
        'recipe': recipe
    })


# ===============================
# AÑADIR INGREDIENTE
# ===============================
@login_required
def add_ingredient(request, recipe_pk):

    recipe = get_object_or_404(Recipe, pk=recipe_pk)

    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()

            return redirect('recipe_detail', pk=recipe.pk)

    else:
        form = RecipeIngredientForm()

    return render(request, 'recipes/add_ingredient.html', {
        'form': form,
        'recipe': recipe
    })


# ===============================
# EDITAR INGREDIENTE
# ===============================
@login_required
def edit_ingredient(request, pk):

    ingredient = get_object_or_404(RecipeIngredient, pk=pk)

    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST, instance=ingredient)

        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=ingredient.recipe.pk)

    else:
        form = RecipeIngredientForm(instance=ingredient)

    return render(request, 'recipes/add_ingredient.html', {
        'form': form,
        'recipe': ingredient.recipe
    })


# ===============================
# ELIMINAR INGREDIENTE
# ===============================
@login_required
def delete_ingredient(request, pk):

    ingredient = get_object_or_404(RecipeIngredient, pk=pk)
    recipe_pk = ingredient.recipe.pk

    ingredient.delete()

    return redirect('recipe_detail', pk=recipe_pk)


# ===============================
# SISTEMA DE VOTACIÓN
# ===============================
@login_required
def vote_experiment(request, pk):

    experiment = get_object_or_404(Experiment, pk=pk)

    vote, created = ExperimentVote.objects.get_or_create(
        experiment=experiment,
        user=request.user
    )

    if created:
        experiment.votes += 1
        experiment.save()
        messages.success(request, "Your vote has been recorded 👍")

    else:
        messages.warning(request, "You already voted for this experiment.")

    return redirect('recipe_detail', pk=experiment.original_recipe.pk)


# ===============================
# ESTADÍSTICAS
# ===============================
def statistics(request):

    # Recipes by difficulty
    difficulty_stats = Recipe.objects.values('difficulty').annotate(total=Count('id'))

    difficulty_labels = [item['difficulty'] for item in difficulty_stats]
    difficulty_data = [item['total'] for item in difficulty_stats]


    # Recipes by user
    user_stats = Recipe.objects.values('created_by__username').annotate(total=Count('id'))

    user_labels = [item['created_by__username'] for item in user_stats]
    user_data = [item['total'] for item in user_stats]


    # Recipes per month
    month_stats = (
        Recipe.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
    )

    month_labels = [str(item['month']) for item in month_stats]
    month_data = [item['total'] for item in month_stats]


    # Most used ingredients
    ingredient_stats = (
        RecipeIngredient.objects
        .values('ingredient__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )

    ingredient_labels = [item['ingredient__name'] for item in ingredient_stats]
    ingredient_data = [item['total'] for item in ingredient_stats]


    # Experiments per recipe
    experiment_stats = (
        Recipe.objects
        .annotate(total_experiments=Count('experiments'))
        .values('title', 'total_experiments')
        .order_by('-total_experiments')[:10]
    )

    experiment_labels = [item['title'] for item in experiment_stats]
    experiment_data = [item['total_experiments'] for item in experiment_stats]


    return render(request, 'recipes/statistics.html', {

        'difficulty_labels': difficulty_labels,
        'difficulty_data': difficulty_data,

        'user_labels': user_labels,
        'user_data': user_data,

        'month_labels': month_labels,
        'month_data': month_data,

        'ingredient_labels': ingredient_labels,
        'ingredient_data': ingredient_data,

        'experiment_labels': experiment_labels,
        'experiment_data': experiment_data
    })


# ===============================
# TOP RECIPES
# ===============================
def top_recipes(request):

    recipes = (
        Recipe.objects
        .annotate(experiment_count=Count('experiments'))
        .order_by('-experiment_count')[:3]
    )

    return render(request, 'recipes/top_recipes.html', {
        'recipes': recipes
    })


# ===============================
# REGISTRO
# ===============================
def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'recipes/signup.html', {
        'form': form
    })