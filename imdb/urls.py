from django.urls import path
from . import views

urlpatterns = [
    path('search-movies/<query_string>/', views.search_movies, name='search_movie'),
    path('get-movie/<int:movie_id>/', views.get_movie_by_id, name='get_movie'),
    path('create-movie/', views.create_movies, name='create_movie'),
    path('update-movies/<int:movie_id>/', views.update_movies, name='update_movie'),
    path('delete-movies/<int:movie_id>/', views.delete_movies, name='delete_movie'),
]