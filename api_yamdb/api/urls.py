from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/', include('djoser.urls')),
    # path('v1/auth/', include('djoser.urls.jwt')),
]
