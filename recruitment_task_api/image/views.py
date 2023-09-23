from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from link.generate_expiring_link import generate_expiring_link
from .processing import process_image
from .serializers import ImageSerializer
from .models import Image
from user.models import User


class ImageViewSet(viewsets.GenericViewSet):
    queryset = Image.objects.none()
    serializer_class = ImageSerializer


class ImageCreateViewSet(mixins.CreateModelMixin,
                         ImageViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data['content']
        user = User.objects.get(email=serializer.validated_data['user'])
        try:  # Attempt to get account tier
            account_tier = user.userprofile.account_tier
        except KeyError:
            return Response(
                {'message': 'Account tier not found'},
                status.HTTP_400_BAD_REQUEST
            )

        try:  # Attempt to get account tier size
            account_tier_size = account_tier.size
            image_urls = process_image(image, account_tier_size,
                                       account_tier.has_original, user.id)

        except Exception:
            return Response(
                {'message': 'Your account tier has no size'},
                status=status.HTTP_400_BAD_REQUEST
            )

        default_response = {
            'message': 'The image has been saved to the database',
            'links': image_urls,
        }

        try:  # Attempt to get expire_time from request
            if account_tier.has_expiring_link:
                expire_time = serializer.validated_data['expire_time']
                expiring_link = generate_expiring_link(image_urls[0], expire_time)
                expiring_link = f'http://localhost:8000/api/images/link/{expiring_link}'
                return Response(
                    {
                        'message': 'The image has been saved to the database',
                        'links': image_urls,
                        'expiring_link': expiring_link
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                raise KeyError
        except KeyError:
            return Response(
                default_response,
                status=status.HTTP_201_CREATED
            )


class ImageRetrieveViewSet(mixins.RetrieveModelMixin, ImageViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            user = kwargs.get('user')
            user = User.objects.get(id=user)
            images = Image.objects.filter(user=user)
            serializer = self.serializer_class(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Unable to fetch images'}, status=status.HTTP_400_BAD_REQUEST)
