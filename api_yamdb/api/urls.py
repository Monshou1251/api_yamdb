from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import JWTToken, Signup, UsersViewSet

app_name = 'api'

router = DefaultRouter()
router.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/auth/token/', JWTToken.as_view(), name='get_token'),
    path('v1/auth/signup/', Signup.as_view(), name='signup'),
    path('v1/', include(router.urls)),
]
