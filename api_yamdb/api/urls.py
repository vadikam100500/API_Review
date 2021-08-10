from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r'nazvanie', views.nazvanie_view)

urlpatterns = [
    path('v1/', include(router.urls)),
]
