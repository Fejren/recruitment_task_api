from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .processing import process_image
from .serializers import ImageSerializer
from .models import Image
from user.models import User


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
            file_names = process_image(image, account_tier, user.id)
            return Response(
                {
                    'message': 'The image has been saved to the database',
                    'links': file_names,
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
