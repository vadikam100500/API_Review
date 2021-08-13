from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import CustomUserSerializer
from .permissions import IsSuperUser, IsAdminUserOrReadOnly
from reviews.models import Title, Genre, Category
from . import serializers
from .filters import Filter

User = get_user_model()


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = request.data.get('confirmation_code')
        username = request.data.get('username')
        if confirmation_code:
            serializer = serializers.ConfirmationCodeSerializer(
                data=self.request.data
            )
            if serializer.is_valid():
                user = get_object_or_404(User, username=username)
                if default_token_generator.check_token(
                    user, confirmation_code
                ):
                    token = AccessToken.for_user(user)
                    return Response(
                        {'token': str(token)}, status=status.HTTP_200_OK
                    )
                return Response(
                    {'confirmation_code': 'confirmation_code is uncorrect'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            self.confirmation_code(request)
        serializer = serializers.SignupSerializer(data=self.request.data)
        if serializer.is_valid() and username != 'me':
            serializer.save()
            self.confirmation_code(request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def confirmation_code(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Confirmation code',
            f'{confirmation_code}',
            f'{settings.ADMIN_EMAIL}',
            [f'{email}'],
            fail_silently=False,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUser,)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, pk=None):
        if request.method == 'GET':
            serializer = CustomUserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=self.request.user)
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(role=user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=(Avg('reviews__score')))
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = Filter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleReadSerializer
        return serializers.TitleCreateSerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'
