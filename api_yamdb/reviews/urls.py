from rest_framework.routers import DefaultRouter
from django.urls import include, path

from reviews.views import ReviewViewSet, CommentViewSet


app_name = 'reviews'

router = DefaultRouter()
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('comments', CommentViewSet, basename='comments')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
