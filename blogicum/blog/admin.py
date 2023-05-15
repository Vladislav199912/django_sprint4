from django.contrib import admin

from .models import Post, Category, Comment, Location

admin.site.empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )


admin.site.register(Category, CategoryAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )


admin.site.register(Location, LocationAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'created_at'
    )


admin.site.register(Comment, CommentAdmin)
