from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserTestCase(TestCase):

    def test_register_ok(self):
        response = self.client.post(
            '/user/register/',
            {
                "username": "admintest",
                "email": "admin@gmail.com",
                "password": "password",
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_register_bad_data(self):
        response = self.client.post(
            '/user/register/',
            {
                "first_name": "admintest",
                "last_name": "admin@gmail.com",
                "pass": "password",
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_register_unique_data(self):
        self.client.post(
            '/user/register/',
            {
                "username": "unique_name1",
                "email": "unique_name1@gmail.com",
                "password": "password",
            }
        )

        response = self.client.post(
            '/user/register/',
            {
                "username": "unique_name2",
                "email": "unique_name2@gmail.com",
                "password": "password",
            }
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            '/user/register/',
            {
                "username": "unique_name1",
                "email": "unique_name1@gmail.com",
                "password": "password",
            }
        )
        self.assertEqual(response.status_code, 400)
