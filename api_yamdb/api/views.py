from django.conf import settings
from django.core.mail import send_mail
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from .permissions import IsAdminOnly
from .serializers import (SignUpSerializer, TokenSerializer,
                          UserForAdminSerializer, UserSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Работа с пользователями
    """
    queryset = User.objects.all()
    serializer_class = UserForAdminSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated, ),
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserForAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)


class Signup(APIView):
    """
    Получить код подтверждения по email.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            email_body = (
                f'Пользователь {user.username} успешно зарегистрирован!'
                f'\nКод подтвержения для доступа к API: '
                f'{user.confirmation_code}'
            )
            send_mail(
                'Код подтвержения для доступа к API!',
                email_body,
                settings.EMAIL_ADMIN,
                recipient_list=[user.email],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JWTToken(APIView):
    """
    Получение JWT-токена по username и confirmation code.
    """
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.get(username=data['username'])
            return Response(
                {'token': str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
