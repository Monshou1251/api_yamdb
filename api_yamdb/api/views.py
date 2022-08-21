from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Title, Review

from .filters import TitleFilter
from .mixins import CustomViewSet
from .permissions import IsAdminOnly, IsAdminUserOrReadOnly, IsStaffOrAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserForAdminSerializer,
                          UserSerializer)

User = get_user_model()


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


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Проставление оценок(score) для публикаций.
    Получение оценки по id публикации.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Комментирование оценок(score) к публикациям.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
