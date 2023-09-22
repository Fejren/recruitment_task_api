import uuid

from django.db import models


class ExpiringLink(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image = models.URLField()
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ('-expires_at',)

    def __str__(self):
        return f'Link expires at {self.expires_at.date()}'
