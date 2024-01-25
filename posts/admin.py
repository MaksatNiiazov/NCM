from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Post, PostImage, Category, Tag


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class PostAdmin(TranslationAdmin):
    fields = ['title', 'text', 'categories', 'tags']
    inlines = [PostImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
