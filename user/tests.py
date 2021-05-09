from django.test import TestCase, Client
from .models import User
from .serializers import TokenSerializer
from django.urls import reverse


class RegisterTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_registration(self):
        url = reverse('register_api')

        # test req method POST with invalid data
        req_data = {
            'name': 'test',
            'email': 'user@test.com',
            'phone': '1234567890',
            'password_1': 'secret',
            'password_2': 'secret1',
        }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status, 400)
        exp_data = {'msg': 'Password does not match.'}
        self.asssertEqual(exp_data, response.json())

        # test req method POST with valid data
        req_data = {
            'name': 'test',
            'email': 'user@test.com',
            'phone': '1234567890',
            'password_1': 'secret',
            'password_2': 'secret',
        }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status, 201)
        exp_data = {'msg': 'User successfully registered.'}
        self.asssertEqual(exp_data, response.json())


class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test2@example.com', password='12test12', name='test', phone='1234567890')
        self.user.save()

    def test_registration(self):
        url = reverse('login_api')

        # test req method POST with invalid data
        req_data = {
            'email': 'test2@example.com',
            'password': '12test1',
        }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status, 401)
        exp_data = {'msg': 'Invalid credentials.'}
        self.asssertEqual(exp_data, response.json())

        # test req method POST with valid data
        req_data = {
             'email': 'test2@example.com',
             'password': '12test12',
        }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status, 200)
        user = User.objects.get(email=req_data['email'])
        data = {
            "user": user,
            "token": user.token()
        }
        exp_data = {'success': True, 'msg': 'Verification success', 'data': TokenSerializer(data).data}
        self.asssertEqual(exp_data, response.json())

