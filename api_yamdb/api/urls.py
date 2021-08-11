from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'titles', views.TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router.urls)),
]
