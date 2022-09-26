from django.contrib import admin
from .models import Category, Post, Author, Comment, PostCategory


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)

nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'type', 'time_in', 'title', 'preview', 'rating')  # fields to display
    list_filter = ('type', 'time_in')                                           # filters
    search_fields = ('author__user__username', 'title__icontains')              # search bar
    actions = [nullfy_rating]                               # add actions to list


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username', )
    actions = [nullfy_rating]                               # add actions to list


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'preview', 'time_in', 'rating')
    list_filter = ('time_in', )
    search_fields = ('user__username', 'post__title__icontains', 'post__text__icontains')
    actions = [nullfy_rating]                               # add actions to list


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'post')
    list_filter = ('category',)
    search_fields = ('post__title__icontains', 'post__text__icontains')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
