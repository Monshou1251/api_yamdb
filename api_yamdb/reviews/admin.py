from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_id', 'text', 'author', 'pub_date')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
