from django.urls import include, path
from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', views.UserViewSet, basename='user')
router_v1.register(r'categories', views.CategoryViewSet, basename='category')
router_v1.register(r'genres', views.GenreViewSet, basename='genre')
router_v1.register(r'titles', views.TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    views.ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    views.CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.SignupView.as_view()),
    path('v1/auth/token/', views.ConfirmationView.as_view())
]
