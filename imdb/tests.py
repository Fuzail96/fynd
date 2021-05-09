from django.test import RequestFactory,TestCase, Client
from django.urls import reverse
from .models import Movie, Genre
from ..user.models import User
from rest_framework.permissions import IsAdminUser
from .views import create_movies, update_movies, delete_movies


class SearchAndGetMovies(TestCase):
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Drama')
        self.genre.save()
        self.movie = Movie.objects.create(name='movie1', director='test_director', popularity=89.0, imdb_score=8.9)
        self.movie.save()
        self.movie.genre.add(*[self.genre])

    def test_search(self):
        # test with no query string
        url = reverse('search_movie', args=(None,))
        response = self.client.get(url)
        self.assertEqual(response.status, 400)
        resp_data = {'msg': 'invalid input for lookup.'}
        self.assertEqual(resp_data, response.json())

        # test with query string
        url = reverse('search_movie', args=('mo',))
        response = self.client.get(url)
        self.assertEqual(response.status, 200)
        resp_data = {"data": [{"id": 1, "genre": [{"id": 1, "name": "Drama"}], "name": "movie1", "director":
                     "test_director", "popularity": 89, "imdb_score": 8.9}]}
        self.assertEqual(resp_data, response.json())

    def test_get_movie(self):
        # test with id which doesn't exists.
        url = reverse('get_movie', args=(2,))
        response = self.client.get(url)
        self.assertEqual(response.status, 400)
        resp_data = {'msg': 'Movie does not exist.'}
        self.assertEqual(resp_data, response.json())

        # test with id which exists.
        url = reverse('get_movie', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status, 200)
        resp_data = {'data': {"id": 1, "genre": [{"id": 1, "name": "Drama"}], "name": "movie1", "director":
                     "test_director", "popularity": 89, "imdb_score": 8.9}}
        self.assertEqual(resp_data, response.json())


class AllMovieTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(email='admin2@example.com', password='admintest12', name='test_admin',
                                             phone='1234567890', is_staff=True)
        self.admin.save()
        self.user = User.objects.create_user(email='user2@example.com', password='usertest12', name='test_user',
                                              phone='0987654321')
        self.user.save()
        self.factory = RequestFactory()

    def create_movie(self):
        # test with admin access.
        url = reverse('create_movie')
        req_data = {
            "genre": [
                {
                    "name": "Crime"
                }
            ],
            "name": "Movie2",
            "director": "test_director2",
            "popularity": 67.0,
            "imdb_score": 6.7
        }
        request = self.factory.post(url, req_data)
        request.user = self.admin
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = create_movies(request)
        self.assertEqual(response.status, 201)
        resp_data = {'msg': 'Movie created.'}
        self.assertEqual(resp_data, response.json())

        # test with user access.
        request.user = self.user
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = create_movies(request)
        self.assertEqual(response.status, 403)
        resp_data = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(resp_data, response.json())

    def update_movie(self):
        # test with admin access.
        url = reverse('update_movie', args=(1,))
        req_data = {
            "genre": [
                {
                    "name": "Drama"
                }
            ],
            "name": "Movie21",
            "director": "test_director21",
            "popularity": 63.0,
            "imdb_score": 6.3
        }
        request = self.factory.post(url, req_data)
        request.user = self.admin
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = update_movies(request)
        self.assertEqual(response.status, 200)
        resp_data = {'msg': 'Movie updated.'}
        self.assertEqual(resp_data, response.json())

        # test with id which doesn't exist.
        url = reverse('update_movie', args=(8,))
        req_data = {
            "genre": [
                {
                    "name": "Drama"
                }
            ],
            "name": "Movie21",
            "director": "test_director21",
            "popularity": 63.0,
            "imdb_score": 6.3
        }
        request = self.factory.post(url, req_data)
        request.user = self.admin
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = update_movies(request)
        self.assertEqual(response.status, 400)
        resp_data = {'msg': 'Movie does not exist.'}
        self.assertEqual(resp_data, response.json())

        # test with user access.
        request.user = self.user
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = update_movies(request)
        self.assertEqual(response.status, 403)
        resp_data = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(resp_data, response.json())

    def delete_movie(self):
        # test with admin access.
        url = reverse('delete_movie', args=(1,))
        request = self.factory.post(url)
        request.user = self.admin
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = delete_movies(request)
        self.assertEqual(response.status, 200)
        resp_data = {'msg': 'Movie deleted.'}
        self.assertEqual(resp_data, response.json())

        # test with id which doesn't exist.
        url = reverse('update_movie', args=(8,))
        request = self.factory.post(url)
        request.user = self.admin
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = delete_movies(request)
        self.assertEqual(response.status, 400)
        resp_data = {'msg': 'Movie does not exist.'}
        self.assertEqual(resp_data, response.json())

        # test with user access.
        request.user = self.user
        permission_check = IsAdminUser()
        permission = permission_check.has_permission(request, None)
        self.assertTrue(permission)
        response = delete_movies(request)
        self.assertEqual(response.status, 403)
        resp_data = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(resp_data, response.json())