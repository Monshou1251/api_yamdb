from rest_framework import serializers
from rest_framework.exceptions import NotFound

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio',
                  'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio',
                  'role']
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise NotFound('Пользователь не найден!')

        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения!')

        return data


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('author', 'title', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'pub_date')
