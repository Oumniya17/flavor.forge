from django import forms
from .models import Recipe, Ingredient, Rating, Experiment, RecipeIngredient


# FORMULARIO RECETA
class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'cooking_time',
            'difficulty',
            'instructions',
            'image'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

        error_messages = {
            'title': {
                'required': 'The recipe must have a title.',
                'max_length': 'Title is too long.'
            },
            'description': {
                'required': 'Please add a description for the recipe.',
            },
            'cooking_time': {
                'required': 'Cooking time is required.',
                'invalid': 'Cooking time must be a number.',
            }
        }


# FORMULARIO INGREDIENTE
class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'category', 'calories']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'})
        }

        error_messages = {
            'name': {
                'required': 'Ingredient name is required.',
                'max_length': 'Ingredient name is too long.'
            },
            'category': {
                'required': 'Please specify a category.',
            },
            'calories': {
                'required': 'Calories value is required.',
                'invalid': 'Calories must be a number.',
            }
        }


# FORMULARIO RATING
class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['score', 'comment']

        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }

        error_messages = {
            'score': {
                'required': 'You must give a rating.',
                'invalid': 'Rating must be between 1 and 5.',
            },
            'comment': {
                'required': 'You can leave a comment.',
                'max_length': 'Comment is too long.'
            }
        }


# FORMULARIO EXPERIMENT
class ExperimentForm(forms.ModelForm):

    class Meta:
        model = Experiment
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }

        error_messages = {
            'title': {
                'required': 'Experiment must have a title.',
                'max_length': 'Title is too long.'
            },
            'description': {
                'required': 'Please describe the experiment.',
            }
        }


# FORMULARIO PARA AÑADIR INGREDIENTES A RECETA
class RecipeIngredientForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
        }

        error_messages = {
            'ingredient': {
                'required': 'Please select an ingredient.'
            },
            'quantity': {
                'required': 'Please specify a quantity.',
                'invalid': 'Quantity must be a number.'
            },
            'unit': {
                'required': 'Please select a unit.'
            }
        }