from datetime import timedelta

from django.utils import timezone

from .models import ExpiringLink


def generate_expiring_link(image_url: str, expire_time: int):
    # Creating a link expiration date
    expiration = timezone.now() + timedelta(seconds=expire_time)
    link = ExpiringLink(image=image_url, expires_at=expiration)
    link.save()
    return link.id
