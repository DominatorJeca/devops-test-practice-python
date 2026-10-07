import json
from .models import User
from django.urls import reverse
from rest_framework.test import APITestCase

class TestUserView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name='Test1', dni='09876543210')
        self.url = reverse('users-list')
        self.data = {'name': 'Test2', 'dni': '09876543211'}

    def test_post(self):
        response = self.client.post(self.url, self.data, format='json')
        body = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['name'], 'Test2')
        self.assertEqual(body['dni'], '09876543211')
        self.assertEqual(User.objects.count(), 2)

    def test_post_duplicate_dni_returns_400(self):
        response = self.client.post(
            self.url, {'name': 'Otro', 'dni': self.user.dni}, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_post_missing_name_returns_400(self):
        response = self.client.post(self.url, {'dni': '11111111111'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get(self):
        response = self.client.get(f'{self.url}{self.user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'id': self.user.id, 'name': 'Test1', 'dni': '09876543210'},
        )

    def test_get_unknown_id_returns_404(self):
        response = self.client.get(f'{self.url}{self.user.id + 999}/')
        self.assertEqual(response.status_code, 404)

class TestHealthEndpoints(APITestCase):
    def test_liveness(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'ok')

    def test_readiness(self):
        response = self.client.get(reverse('ready'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['database'], 'up')