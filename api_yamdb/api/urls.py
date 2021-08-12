from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'titles', views.TitleViewSet, basename='title')
router.register(r'^titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='review')
router.register(r'^reviews/^(?P<review_id>\d+)/comments',
                views.CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
]
