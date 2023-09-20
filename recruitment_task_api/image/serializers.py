from rest_framework import serializers

from PIL import Image as ProcessImage

from .models import Image


def validate_format(content):
    allowed_formats = ('jpeg', 'jpg', 'png')  # only these formats are allowed
    img = ProcessImage.open(content)
    img_format = img.format.lower()
    if img_format not in allowed_formats:
        raise serializers.ValidationError("Only jpg and png formats are allowed")


class ImageSerializer(serializers.ModelSerializer):
    content = serializers.ImageField(validators=[validate_format])

    class Meta:
        model = Image
        fields = '__all__'
