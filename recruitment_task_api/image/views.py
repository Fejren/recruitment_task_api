from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .serializers import ImageSerializer
from .models import Image
from PIL import Image as ProcessImage
from user.models import User, AccountTier


def process_image(image, account_tier: AccountTier, user_id: int) -> None:
    img = ProcessImage.open(image.content)
    images = []
    for size in account_tier.size:
        proportion: float = (size / float(img.size[1]))
        width = int((float(img.size[0]) * proportion))
        img = img.resize((width, size))
        images.append(img)

    Image.objects.create(content=image.content, user_id=user_id)
    for i in images:
        Image.objects.create(content=i, user_id=user_id)


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

            saved_image = Image.objects.create(content=image, user_id=user.id)
            process_image(saved_image, account_tier, user.id)

            return Response({'message': 'Obraz przetworzony pomyślnie'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
