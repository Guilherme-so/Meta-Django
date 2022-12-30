from django.urls import path, include
from . import views

# class_based_views

# urlpatterns = [
#     path('livros/', views.LivrosView.as_view()),
#     path('livros/<int:pk>/', views.SingleLivroView.as_view()),
#     path('categories/', views.CategoriesView.as_view()),
#     path('categories/<int:pk>/', views.SingleCategory.as_view()),

# ]


# ====================================================================================================


# functions_base_views

urlpatterns = [
    path('livros/', views.livros),
    path('livros/<int:pk>/', views.livro),
    path('categories/', views.categories),
    path('categories/<int:id>/', views.singleCategory),
    path('aluguei-group-add-user', views.aluguel),
]
