from django.urls import path
from . import views

urlpatterns = [
    path('search-movies/<query_string>/', views.search_movies),
    path('create-movie/', views.create_movies),
    path('update-movies/<movie_id>/', views.update_movies),
    path('delete-movies/<movie_id>/', views.delete_movies),
]