from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .serializers import ImageSerializer
from .models import Image
from PIL import Image as ProcessImage
from user.models import User, AccountTier


def process_image(image_file, account_tier: AccountTier, user_id: int) -> None:
    img = ProcessImage.open(image_file.content)
    images = []
    for size in account_tier.size:
        proportion = size / float(img.size[1])
        width = int(float(img.size[0]) * proportion)
        img_resized = img.resize((width, size))
        images.append(img_resized)

    # Create Image objects for the resized images
    for i in images:
        # Convert PIL.Image to bytes
        image_bytes = BytesIO()
        i.save(image_bytes, format='JPEG')  # You can choose the desired format
        image_bytes.seek(0)

        # Create SimpleUploadedFile
        file_name = f"{user_id}_resized_{account_tier.size}.jpg"
        resized_image = SimpleUploadedFile(file_name, image_bytes.read())
        Image.objects.create(content=resized_image, user_id=user_id)


class ImageCreateAndRetrieveViewSet(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    queryset = Image.objects.none()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['content']
            user = User.objects.get(email=serializer.validated_data['user'])
            account_tier = user.userprofile.account_tier
            if account_tier is None:
                return Response({'message': 'Account tier not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if account_tier.size is None:
                    return Response({'message': 'Your account tier has no size'}, status=status.HTTP_400_BAD_REQUEST)
            saved_image = Image.objects.create(content=image, user_id=user.id)
            process_image(saved_image, account_tier, user.id)

            return Response({'message': 'Obraz przetworzony pomyślnie'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
