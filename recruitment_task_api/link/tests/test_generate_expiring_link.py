from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from link.models import ExpiringLink
from link.generate_expiring_link import generate_expiring_link, is_link_expired


def expiring_link_for_image_url(link_id):
    return reverse('link:expiring-link-retrieve', args=[link_id])


IMAGE_URL = 'https://example.com/image.jpg'


class ExpiringLinkTestCase(TestCase):

    def test_generate_expiring_link(self):
        expire_time = 3600  # 1 hour in seconds

        link_id = generate_expiring_link(IMAGE_URL, expire_time)

        # Check if the link was created
        link = ExpiringLink.objects.get(id=link_id)
        self.assertEqual(link.image, IMAGE_URL)

    def test_is_link_expired(self):
        # Test that link is expired
        expire_time = 30
        link_id = generate_expiring_link(IMAGE_URL, expire_time)

        # Ensure the link is initially not expired
        link = ExpiringLink.objects.get(id=link_id)
        self.assertFalse(is_link_expired(link))

        # Check if the link is now expired
        link.refresh_from_db()
        current_time = timezone.now() + timedelta(seconds=expire_time + 10)
        self.assertTrue(link.expires_at <= current_time)

    def test_retrieve_image(self):
        # Create an expired link
        expire_time = 30
        link_id = generate_expiring_link(IMAGE_URL, expire_time)

        # Try to retrieve the expired link
        response = self.client.get(expiring_link_for_image_url(link_id))

        # Check if the response status code is 302 (Redirect)
        self.assertEqual(response.status_code, 302)

    def test_expired_link(self):
        # Create an expired link
        expire_time = 0
        link_id = generate_expiring_link(IMAGE_URL, expire_time)

        # Try to retrieve the expired link
        response = self.client.get(expiring_link_for_image_url(link_id))

        # Check if the response status code is 400 (Bad Request) because link is expired
        self.assertEqual(response.status_code, 400)
