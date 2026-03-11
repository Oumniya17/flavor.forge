from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from recipes.models import Recipe, Ingredient, RecipeIngredient, Experiment
from recipes.forms import RecipeForm, IngredientForm


# =====================
# BASE TEST
# =====================

class BaseTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="chef",
            password="123"
        )

        self.recipe = Recipe.objects.create(
            title="Test recipe",
            description="desc",
            cooking_time=10,
            difficulty="easy",
            instructions="cook",
            created_by=self.user
        )

        self.ingredient = Ingredient.objects.create(
            name="Tomato",
            category="Vegetable",
            calories=20
        )


# =====================
# MODEL TESTS
# =====================

class RecipeModelTests(BaseTest):

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, "Test recipe")

    def test_recipe_description(self):
        self.assertEqual(self.recipe.description, "desc")

    def test_recipe_time(self):
        self.assertEqual(self.recipe.cooking_time, 10)

    def test_recipe_difficulty(self):
        self.assertEqual(self.recipe.difficulty, "easy")

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), "Test recipe")


class IngredientModelTests(BaseTest):

    def test_ingredient_name(self):
        self.assertEqual(self.ingredient.name, "Tomato")

    def test_ingredient_category(self):
        self.assertEqual(self.ingredient.category, "Vegetable")

    def test_ingredient_calories(self):
        self.assertEqual(self.ingredient.calories, 20)

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), "Tomato")

    def test_ingredient_unique(self):
        with self.assertRaises(Exception):
            Ingredient.objects.create(
                name="Tomato",
                category="Vegetable",
                calories=20
            )


class RecipeIngredientTests(BaseTest):

    def test_create_recipeingredient(self):
        ri = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=100,
            unit="g"
        )
        self.assertEqual(ri.quantity, 100)

    def test_recipeingredient_unit(self):
        ri = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=1,
            unit="unit"
        )
        self.assertEqual(ri.unit, "unit")

    def test_recipeingredient_relation(self):
        ri = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=50,
            unit="g"
        )
        self.assertEqual(ri.recipe, self.recipe)

    def test_recipeingredient_ingredient(self):
        ri = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=50,
            unit="g"
        )
        self.assertEqual(ri.ingredient, self.ingredient)

    def test_recipeingredient_str(self):
        ri = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=10,
            unit="g"
        )
        self.assertIn("Tomato", str(ri))


class ExperimentModelTests(BaseTest):

    def test_create_experiment(self):
        experiment = Experiment.objects.create(
            original_recipe=self.recipe,
            title="Salt",
            description="Try salt",
            created_by=self.user
        )
        self.assertEqual(experiment.title, "Salt")

    def test_experiment_description(self):
        experiment = Experiment.objects.create(
            original_recipe=self.recipe,
            title="Test",
            description="Example",
            created_by=self.user
        )
        self.assertEqual(experiment.description, "Example")

    def test_experiment_recipe(self):
        experiment = Experiment.objects.create(
            original_recipe=self.recipe,
            title="Test",
            description="desc",
            created_by=self.user
        )
        self.assertEqual(experiment.original_recipe, self.recipe)

    def test_experiment_user(self):
        experiment = Experiment.objects.create(
            original_recipe=self.recipe,
            title="Test",
            description="desc",
            created_by=self.user
        )
        self.assertEqual(experiment.created_by, self.user)

    def test_experiment_str(self):
        experiment = Experiment.objects.create(
            original_recipe=self.recipe,
            title="Salt",
            description="desc",
            created_by=self.user
        )
        self.assertEqual(str(experiment), "Salt")


# =====================
# FORM TESTS
# =====================

class RecipeFormTests(TestCase):

    def test_recipe_form_valid(self):
        form = RecipeForm(data={
            "title": "Test",
            "description": "desc",
            "cooking_time": 10,
            "difficulty": "easy",
            "instructions": "cook"
        })
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid_empty(self):
        form = RecipeForm(data={})
        self.assertFalse(form.is_valid())

    def test_recipe_form_missing_title(self):
        form = RecipeForm(data={
            "description": "desc",
            "cooking_time": 10,
            "difficulty": "easy",
            "instructions": "cook"
        })
        self.assertFalse(form.is_valid())

    def test_recipe_form_invalid_time(self):
        form = RecipeForm(data={
            "title": "Test",
            "description": "desc",
            "cooking_time": "",
            "difficulty": "easy",
            "instructions": "cook"
        })
        self.assertFalse(form.is_valid())

    def test_recipe_form_difficulty_choice(self):
        form = RecipeForm(data={
            "title": "Test",
            "description": "desc",
            "cooking_time": 10,
            "difficulty": "medium",
            "instructions": "cook"
        })
        self.assertTrue(form.is_valid())


class IngredientFormTests(TestCase):

    def test_ingredient_form_valid(self):
        form = IngredientForm(data={
            "name": "Onion",
            "category": "Vegetable",
            "calories": 30
        })
        self.assertTrue(form.is_valid())

    def test_ingredient_form_invalid_empty(self):
        form = IngredientForm(data={})
        self.assertFalse(form.is_valid())

    def test_ingredient_form_missing_name(self):
        form = IngredientForm(data={
            "category": "Vegetable",
            "calories": 20
        })
        self.assertFalse(form.is_valid())

    def test_ingredient_form_missing_category(self):
        form = IngredientForm(data={
            "name": "Carrot",
            "calories": 10
        })
        self.assertFalse(form.is_valid())

    def test_ingredient_form_invalid_calories(self):
        form = IngredientForm(data={
            "name": "Carrot",
            "category": "Vegetable",
            "calories": ""
        })
        self.assertFalse(form.is_valid())


# =====================
# VIEW TESTS
# =====================

class ViewTests(BaseTest):

    def test_recipe_list(self):
        response = self.client.get(reverse("recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail(self):
        response = self.client.get(reverse("recipe_detail", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)

    def test_statistics_page(self):
        response = self.client.get(reverse("statistics"))
        self.assertEqual(response.status_code, 200)

    def test_top_recipes_page(self):
        response = self.client.get(reverse("top_recipes"))
        self.assertEqual(response.status_code, 200)


# =====================
# AUTH TESTS
# =====================

class AuthTests(BaseTest):

    def test_recipe_create_requires_login(self):
        response = self.client.get(reverse("recipe_create"))
        self.assertEqual(response.status_code, 302)

    def test_recipe_create_logged(self):
        self.client.login(username="chef", password="123")
        response = self.client.get(reverse("recipe_create"))
        self.assertEqual(response.status_code, 200)

    def test_experiment_create_requires_login(self):
        response = self.client.get(reverse("experiment_create", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)

    def test_experiment_create_logged(self):
        self.client.login(username="chef", password="123")
        response = self.client.get(reverse("experiment_create", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)


# =====================
# PAGINATION TESTS
# =====================

class PaginationTests(TestCase):

    def setUp(self):

        user = User.objects.create(username="chef")

        for i in range(15):
            Recipe.objects.create(
                title=f"Recipe {i}",
                description="desc",
                cooking_time=10,
                difficulty="easy",
                instructions="cook",
                created_by=user
            )

    def test_recipe_pagination(self):
        response = self.client.get(reverse("recipe_list"))
        self.assertEqual(response.status_code, 200)


# =====================
# EXTRA TESTS
# =====================

class ExtraTests(BaseTest):

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):
        user = User.objects.create(username="test")
        self.assertEqual(user.username, "test")