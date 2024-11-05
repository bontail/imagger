from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()
BOUNDARY = "BoUnDaRyStRiNg"
MULTIPART_CONTENT = "multipart/form-data; boundary=%s" % BOUNDARY


class AppTestCase(TestCase):

    def setUp(self):
        self.image = open(
            "/app/public/tests/apple.png", "rb"
        )
        self.first_user = User.objects.create(
            username='test', email="test@gmail.com"
        )
        self.first_user.set_password("test")
        self.first_user.save()
        response = self.client.post(
            "/user/login/",
            {"username": "test", "password": "test"},
        )
        self.first_token = response.json()['access']

        self.second_user = User.objects.create(
            username='test2', email="test2@gmail.com"
        )
        self.second_user.set_password("test2")
        self.second_user.save()
        response = self.client.post(
            "/user/login/",
            {"username": "test2", "password": "test2"},
        )
        self.second_token = response.json()['access']

    def tearDown(self):
        self.image.close()

    def test_create_image_unauthorized(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "image": self.image,
            }
        )
        self.assertEqual(response.status_code, 401)

    def test_create_image_ok(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "description": "my description",
                "resolution": "1000x1000",
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 201)

    def test_create_image_bad_request(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "tags": ['Cats'],
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['None'],
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 400)

    def test_get_image_unauthorized(self):
        response = self.client.get(
            '/app/get_image/1',
        )
        self.assertEqual(response.status_code, 401)

    def test_get_image_not_found(self):
        response = self.client.get(
            '/app/get_image/1',
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 404)

    def test_get_image_ok(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "description": "my description",
                "resolution": "1000x1000",
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )

        response = self.client.get(
            f'/app/get_image/{response.json()['id']}',
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )

        self.assertEqual(response.status_code, 200)

    def test_get_image_private(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "description": "my description",
                "resolution": "1000x1000",
                "image": self.image,
                "is_private": True,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        image_id = response.json()['id']

        response = self.client.get(
            f'/app/get_image/{image_id}',
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f'/app/get_image/{image_id}',
            headers={'Authorization': 'Bearer {}'.format(self.second_token)}
        )
        self.assertEqual(response.status_code, 404)

    def test_update_image_unauthorized(self):
        response = self.client.patch(
            '/app/update_image/1',
        )
        self.assertEqual(response.status_code, 401)

    def test_update_image_not_found(self):
        response = self.client.patch(
            '/app/update_image/1',
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 404)

    def test_update_image_ok(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "description": "my description",
                "resolution": "1000x1000",
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )

        response = self.client.patch(
            f'/app/update_image/{response.json()['id']}',
            content_type=MULTIPART_CONTENT, data={"name": "my new name"},
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )

        self.assertEqual(response.status_code, 200)

    def test_update_image_another(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "description": "my description",
                "resolution": "1000x1000",
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        image_id = response.json()['id']

        response = self.client.patch(
            f'/app/update_image/{image_id}',
            content_type=MULTIPART_CONTENT,
            data={"name": "my new name", "tags": ['Cats']},
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(
            f'/app/update_image/{image_id}',
            {"name": "my new name", "tags": ['Cats']},
            headers={'Authorization': 'Bearer {}'.format(self.second_token)}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_image_unauthorized(self):
        response = self.client.delete(
            '/app/delete_image/1',
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_image_not_found(self):
        response = self.client.delete(
            '/app/delete_image/1',
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_image_ok(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "description": "my description",
                "resolution": "1000x1000",
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )

        response = self.client.delete(
            f'/app/delete_image/{response.json()['id']}',
            content_type=MULTIPART_CONTENT,
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )

        self.assertEqual(response.status_code, 204)

    def test_delete_image_another(self):
        response = self.client.post(
            '/app/create_image/',
            {
                "name": "my image",
                "tags": ['Cats'],
                "description": "my description",
                "resolution": "1000x1000",
                "image": self.image,
            },
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        image_id = response.json()['id']

        response = self.client.delete(
            f'/app/delete_image/{image_id}',
            content_type=MULTIPART_CONTENT,
            headers={'Authorization': 'Bearer {}'.format(self.first_token)}
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(
            f'/app/delete_image/{image_id}',
            headers={'Authorization': 'Bearer {}'.format(self.second_token)}
        )
        self.assertEqual(response.status_code, 404)
