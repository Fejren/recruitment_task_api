from django.contrib.auth import get_user_model
from django.db import models


class Image(models.Model):
    content = models.ImageField(upload_to='static/images/')
    user = models.ForeignKey(
        get_user_model(),
        related_name='user_images',
        on_delete=models.CASCADE, db_index=True
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'Author: {self.user.email} ImageId: {self.id}'
