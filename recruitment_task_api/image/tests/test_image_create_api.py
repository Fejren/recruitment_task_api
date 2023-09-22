import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from django.core.files.uploadedfile import SimpleUploadedFile

from user.models import AccountTier, UserProfile


class ImageCreateAndRetrieveViewSetTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        self.account_tier = AccountTier.objects.create(
            name='Basic',
            size=[200],
            has_original=True,
            has_expiring_link=False
        )
        self.user_profile = UserProfile(
            user_id=self.user.id,
            account_tier_id=self.account_tier.id
        )

        self.client = APIClient()
        self.image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')

        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(f'{self.image_path}', 'rb').read(),
            content_type='image/jpeg'
        )

    def test_create_image_invalid_format(self):
        invalid_image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        with open(invalid_image_path, 'rb') as image_file:
            data = {
                'content': SimpleUploadedFile('test_image.jpg', image_file.read()),
                'user': self.user.id
            }
            response = self.client.post('/api/images/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_image_no_account_tier(self):
        self.account_tier = None
        response = self.client.post('/api/images/', {
            'content': self.image,
            'user': self.user.id
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_image_no_size_in_account_tier(self):
        self.account_tier.size = None
        response = self.client.post('/api/images/', {
            'content': self.image,
            'user': self.user.id
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
