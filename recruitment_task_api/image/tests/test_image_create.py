import json
import os
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.core.files.uploadedfile import SimpleUploadedFile

from user.models import AccountTier, UserProfile

CREATE_IMAGE_URL = reverse('image:image-create')


def create_user_profile(user_id, account_tier_id):
    UserProfile(
        user_id=user_id,
        account_tier_id=account_tier_id
    ).save()


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
        self.premium_tier = AccountTier.objects.create(
            name='Premium',
            size=[200, 400],
            has_original=True,
            has_expiring_link=False
        )
        self.enterprise_tier = AccountTier.objects.create(
            name='Enterprise',
            size=[200, 400],
            has_original=True,
            has_expiring_link=True
        )

        self.client = APIClient()
        self.image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')

        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(f'{self.image_path}', 'rb').read(),
            content_type='image/jpeg'
        )

    def test_create_image_invalid_format(self):
        create_user_profile(self.user.id, self.basic_tier.id)
        invalid_image_path = os.path.join(os.path.dirname(__file__), 'test_invalid_image.gif')
        with open(invalid_image_path, 'rb') as image_file:
            data = {
                'content': SimpleUploadedFile('test_image.jpg', image_file.read()),
                'user': self.user.id
            }
            response = self.client.post(CREATE_IMAGE_URL, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_image_no_account_tier(self):
        create_user_profile(self.user.id, self.basic_tier.id)
        self.basic_tier.delete()
        response = self.client.post(CREATE_IMAGE_URL, {
            'content': self.image,
            'user': self.user.id
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_basic_tier_link_amount_after_create(self):
        create_user_profile(self.user.id, self.basic_tier.id)
        response = self.client.post(CREATE_IMAGE_URL, {
            'content': self.image,
            'user': self.user.id
        }, format='multipart')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(content['links']), 1)

    def test_premium_tier_link_amount_after_create(self):
        create_user_profile(self.user.id, self.premium_tier.id)
        response = self.client.post(CREATE_IMAGE_URL, {
            'content': self.image,
            'user': self.user.id
        }, format='multipart')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(content['links']), 3)

    def test_enterprise_tier_link_amount_after_create(self):
        create_user_profile(self.user.id, self.enterprise_tier.id)
        response = self.client.post(CREATE_IMAGE_URL, {
            'content': self.image,
            'user': self.user.id
        }, format='multipart')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(content['links']), 3)

    def test_enterprise_tier_has_expiring_link_after_create(self):
        create_user_profile(self.user.id, self.enterprise_tier.id)
        response = self.client.post(CREATE_IMAGE_URL, {
            'content': self.image,
            'user': self.user.id,
            'expire_time': 30
        }, format='multipart')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(content['links']), 3)
        self.assertIsNotNone(content['expiring_link'])
