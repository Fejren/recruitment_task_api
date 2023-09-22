from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from link.generate_expiring_link import generate_expiring_link
from .processing import process_image
from .serializers import ImageSerializer
from .models import Image
from user.models import User


class ImageCreateViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Image.objects.none()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['content']
            user = User.objects.get(email=serializer.validated_data['user'])
            try:
                account_tier = user.userprofile.account_tier
            except Exception as e:
                return Response(
                    {'message': 'Account tier not found'},
                    status.HTTP_400_BAD_REQUEST
                )
            if account_tier.size is None:  # If account tier does not contain info about image size
                return Response(
                    {'message': 'Your account tier has no size'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            image_urls = process_image(image, account_tier, user.id)

            if account_tier.has_expiring_link:
                try:
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
                except Exception:
                    return Response(
                        {
                            'message': 'The image has been saved to the database',
                            'links': image_urls,
                        },
                        status=status.HTTP_201_CREATED
                    )
            else:
                return Response(
                    {
                        'message': 'The image has been saved to the database',
                        'links': image_urls,
                    },
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
