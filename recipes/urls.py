from django.urls import path
from . import views

urlpatterns = [

    path('', views.recipe_list),

    path('recipes/', views.recipe_list, name='recipe_list'),

    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),

    path('recipe/new/', views.recipe_create, name='recipe_create'),

    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),

    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),

    path('recipe/<int:recipe_pk>/experiment/new/', views.experiment_create, name='experiment_create'),

    path('recipe/<int:recipe_pk>/ingredient/new/', views.add_ingredient, name='add_ingredient'),

    # NUEVAS RUTAS
    path('ingredient/<int:pk>/edit/', views.edit_ingredient, name='edit_ingredient'),
    
    path('ingredient/<int:pk>/delete/', views.delete_ingredient, name='delete_ingredient'),

    path('experiment/<int:pk>/vote/', views.vote_experiment, name='vote_experiment'),

    path('statistics/', views.statistics, name='statistics'),

    path('top-recipes/', views.top_recipes, name='top_recipes'),

    path('signup/', views.signup, name='signup'),

]