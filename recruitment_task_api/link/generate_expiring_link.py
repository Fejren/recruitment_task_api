from datetime import timedelta

from django.utils import timezone

from .models import ExpiringLink


def generate_expiring_link(image_url: str, expire_time: int):
    # Creating a link expiration date
    expiration = timezone.now() + timedelta(seconds=expire_time)
    link = ExpiringLink(image=image_url, expires_at=expiration)
    link.save()
    return link.id


def is_link_expired(expiring_link_model: ExpiringLink) -> bool:
    # Check if link has expired
    current_time = timezone.now()
    if expiring_link_model.expires_at <= current_time:
        return True
    else:
        return False
