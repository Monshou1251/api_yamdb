from django_filters import filters, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
