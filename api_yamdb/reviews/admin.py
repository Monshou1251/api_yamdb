from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'review_id', 'text', 'author', 'pub_date']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_id', 'text', 'author', 'score', 'pub_date']


class TitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'category']

