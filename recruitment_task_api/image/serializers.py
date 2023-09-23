from rest_framework import serializers

from PIL import Image as ProcessImage

from .models import Image


def validate_format(content):
    allowed_formats = ('jpeg', 'jpg', 'png')  # Only these formats are allowed
    img = ProcessImage.open(content)
    img_format = img.format.lower()
    if img_format not in allowed_formats:
        raise serializers.ValidationError("Only jpg and png formats are allowed")


class ImageSerializer(serializers.ModelSerializer):
    # Add custom validator to content field
    content = serializers.ImageField(validators=[validate_format])
    expire_time = serializers.IntegerField(
        min_value=300,
        max_value=30000,
        required=False
    )

    class Meta:
        model = Image
        fields = '__all__'
