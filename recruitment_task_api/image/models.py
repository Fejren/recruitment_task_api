from django.contrib.auth import get_user_model
from django.db import models


class Image(models.Model):
    content = models.ImageField(upload_to='static/images/',
                                db_index=True)
    user = models.ForeignKey(
        get_user_model(),
        related_name='user_images',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'Author: {self.user.email} ImageId: {self.id}'

    def get_url(self) -> str:
        # Get image url
        file_name = self.content.name
        return f'http://localhost:8000/{file_name}'
