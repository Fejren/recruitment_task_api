import json
import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.core.files.uploadedfile import SimpleUploadedFile

from image.tests.test_image_create import create_user_profile
from user.models import AccountTier

CREATE_IMAGE_URL = reverse('image:image-create')


def retrieve_image_url(user_id):
    return reverse('image:image-retrieve', args=[user_id])


def create_sample_image(client, user_id, image):
    client.post(CREATE_IMAGE_URL, {
        'content': image,
        'user': user_id
    }, format='multipart')


class ImageCreateAndRetrieveViewSetTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        self.basic_tier = AccountTier.objects.create(
            name='Basic',
            size=[200],
            has_original=False,
            has_expiring_link=False
        )

        self.user_profile = create_user_profile(self.user.id,
                                                self.basic_tier.id)

        self.client = APIClient()
        self.image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')

        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(f'{self.image_path}', 'rb').read(),
            content_type='image/jpeg'
        )

    def test_retrieve_images(self):
        create_sample_image(self.client, self.user.id, self.image)
        create_sample_image(self.client, self.user.id, self.image)

        response = self.client.get(retrieve_image_url(self.user.id))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 2)
