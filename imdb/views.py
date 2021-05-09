from rest_framework.response import Response
from django.db.models import Q
from .models import Movie, Genre
from .serializers import MovieSerializer
from . import docs
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser


@swagger_auto_schema(**docs.search_movie)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def search_movies(request, query_string,  *args, **kwargs):
    """
    API view for searching Movies
    """
    movie_serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    try:
        if query_string is not None:
            queryset = queryset.filter(Q(name__icontains=query_string) | Q(director__icontains=query_string)
                                       | Q(genre__name__icontains=query_string) | Q(director__icontains=query_string)).distinct()
            serializer = movie_serializer_class(queryset, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'invalid input for lookup.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'msg': 'Some Execption Occured.', 'Execption': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(**docs.get_movie_by_id)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def get_movie_by_id(request, movie_id,  *args, **kwargs):
    """
    API view for getting Movie by id
    """
    movie_serializer_class = MovieSerializer
    try:
        movie = Movie.objects.filter(id=movie_id)
        if movie.exists():
            return Response({'data': MovieSerializer(movie.first()).data}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Movie does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'msg': 'Some Execption Occured.', 'Execption': e},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(**docs.create_movie)
@csrf_exempt
@api_view(("POST",))
@permission_classes((IsAdminUser,))
def create_movies(request, *args, **kwargs):
    """
    API view for creating Movies
    """
    movie_serializer_class = MovieSerializer
    serializer = movie_serializer_class(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        name = data['name']
        director = data['director']
        genre = data['genre']
        genre_objs = []
        for genre_obj in genre:
            if not Genre.objects.filter(name=genre_obj['name']).exists():
                g = Genre.objects.create(name=genre_obj['name'])
                g.save()
                genre_objs.append(g)
            else:
                g = Genre.objects.get(name=genre_obj['name'])
                genre_objs.append(g)

        popularity = data['popularity']
        imdb_score = data['imdb_score']
        movie = Movie.objects.create(
            name=name,
            director=director,
            popularity=popularity,
            imdb_score=imdb_score
        )
        movie.save()
        movie.genre.add(*genre_objs)
        return Response({'msg': 'Movie created.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'msg': 'Some Execption Occured.', 'Execption': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(**docs.update_movie)
@csrf_exempt
@api_view(("PUT",))
@permission_classes((IsAdminUser,))
def update_movies(request, movie_id, *args, **kwargs):
    """
    API view for update Movies
    """
    movie_serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    serializer = movie_serializer_class(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        name = data['name']
        director = data['director']
        genre = data['genre']
        popularity = data['popularity']
        imdb_score = data['imdb_score']
        movie = Movie.objects.filter(id=movie_id)
        if movie.exists():
            movie_obj = movie.first()
            movie_obj.name = name
            movie_obj.director = director
            movie_obj.genre = genre
            movie_obj.popularity = popularity
            movie_obj.imdb_score = imdb_score
            movie.save()
            return Response({'msg': 'Movie updated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Movie does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'msg': 'Some Execption Occured.', 'Execption': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(**docs.delete_movie)
@csrf_exempt
@api_view(("DELETE",))
@permission_classes((IsAdminUser,))
def delete_movies(request, movie_id, *args, **kwargs):
    """
    API view for deleting Movies
    """
    try:
        movie = Movie.objects.filter(id=movie_id)
        if movie.exists():
            movie.delete()
            return Response({'msg': 'Movie deleted.'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Movie does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'msg': 'Some Execption Occured.', 'Execption': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
