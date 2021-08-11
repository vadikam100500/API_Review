from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import CustomUserSerializer
from .permissions import IsSuperUser

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUser,)
    lookup_field = 'username'
