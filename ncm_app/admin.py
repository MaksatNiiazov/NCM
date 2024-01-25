from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from posts.models import Post
from .models import Page, Block, TextBlock, Slide, SliderBlock, TextWithImageBlock, CardsBlock, Card, Header, \
    CustomHTMLBlock, TextSliderBlock, Footer, SocialLinks


class PostInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Post
    extra = 0


# Базовый админ-класс для блоков
class BaseBlockAdmin(TranslationAdmin):
    block_type = None  # Это должно быть переопределено в подклассах

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if self.block_type and 'block' in form.base_fields:
            form.base_fields['block'].queryset = Block.objects.filter(block_type=self.block_type)
        return form


# BlockInline
class BlockInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Block
    extra = 0


# PageAdmin
@admin.register(Page)
class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'main_page', 'order']
    inlines = [BlockInline]


# HeaderAdmin
@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    pass


class SocialLinksInline(SortableInlineAdminMixin, admin.StackedInline):
    model = SocialLinks
    extra = 1


@admin.register(Footer)
class FooterAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [SocialLinksInline]


# TextBlockAdmin
@admin.register(TextBlock)
class TextBlockAdmin(BaseBlockAdmin):
    block_type = 'text'
    fieldsets = (
        (None, {'fields': ('block',)}),
        ('Block Settings', {'fields': ('background_color', 'margin', 'padding', 'border_radius')}),
        ('Content', {'fields': ('title', 'title_size', 'title_color', 'text', 'text_size', 'text_color')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'block' in form.base_fields:
            form.base_fields['block'].queryset = Block.objects.filter(block_type='text')
        return form


# TextWithImageBlockAdmin
@admin.register(TextWithImageBlock)
class TextWithImageBlockAdmin(BaseBlockAdmin):
    block_type = 'text_image'
    list_display = (
        'block', 'image', 'image_width', 'image_height', 'alt', 'title', 'title_color', 'text_color', 'direction')
    fieldsets = (
        (None, {'fields': ('block',)}),
        ('Block Settings', {'fields': ('direction', 'background_color', 'margin', 'padding', 'border_radius')}),
        ('Image Settings', {'fields': ('image', 'image_width', 'image_height', 'alt')}),
        ('Title Settings', {'fields': ('title', 'title_color', 'title_size')}),
        ('Text Settings', {'fields': ('text', 'text_size', 'text_color')}),
    )


# SlideInline
class SlideInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Slide
    extra = 1
    readonly_fields = ["preview_image"]

    def preview_image(self, obj):
        return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)

    preview_image.short_description = "Preview Image"


# SliderBlockAdmin
@admin.register(SliderBlock)
class SliderBlockAdmin(SortableAdminMixin, BaseBlockAdmin):
    block_type = 'slider'
    list_display = ('block', 'title', 'title_color', 'title_size', 'slides_per_view_desktop', 'slides_per_view_tablet',
                    'slides_per_view_mobile', 'navigation_color')
    fieldsets = (
        (None, {'fields': ('block',)}),
        ('Block Settings', {'fields': ('background_color', 'margin', 'padding', 'border_radius')}),

        ('Slider Settings', {'fields': ('title', 'title_color', 'title_size')}),
        ('View Settings', {'fields': (
            'slides_per_view_desktop', 'slides_per_view_tablet', 'slides_per_view_mobile', 'navigation_color')}),
    )
    inlines = [SlideInline]


# CardInline
class CardInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Card
    extra = 1
    inlines = [PostInline]


# CardsBlockAdmin
@admin.register(CardsBlock)
class CardsBlockAdmin(SortableAdminMixin, BaseBlockAdmin):
    block_type = 'cards'
    list_display = (
        'block', 'title', 'title_color', 'title_size', 'background_color', 'cards_per_row_desktop',
        'cards_per_row_tablet', 'cards_per_row_mobile', 'order')
    fieldsets = (
        (None, {'fields': ('block',)}),
        ('Block Settings', {'fields': ('background_color', 'margin', 'padding', 'border_radius')}),
        ('Card Settings', {'fields': ('title', 'title_color', 'title_size')}),
        ('Layout Settings', {'fields': ('cards_per_row_desktop', 'cards_per_row_tablet', 'cards_per_row_mobile')}),
    )
    inlines = [CardInline]


# TextSliderBlockAdmin
@admin.register(TextSliderBlock)
class TextSliderBlockAdmin(SortableAdminMixin, BaseBlockAdmin):
    block_type = 'text_slider'
    list_display = ('block',)
    fieldsets = (
        (None, {'fields': ('block',)}),
        ('Block Settings', {'fields': ('background_color', 'margin', 'padding', 'border_radius', 'direction')}),
        ('Title Settings', {'fields': ('title', 'title_color', 'title_size')}),
        ('Text Settings', {'fields': ('text', 'text_size', 'text_color')}),
        ('Slider Settings', {'fields': ('navigation_color',)}),

    )
    inlines = [SlideInline]


# CustomHTMLBlockAdmin
@admin.register(CustomHTMLBlock)
class CustomHTMLBlockAdmin(admin.ModelAdmin):
    list_display = ('block', 'name')
    fieldsets = (
        (None, {'fields': ('block', 'name')}),
        ('Block Settings', {'fields': ('background_color', 'margin', 'padding', 'border_radius')}),
        ('HTML Content', {'fields': ('html_content',)}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if self.block_type and 'block' in form.base_fields:
            form.base_fields['block'].queryset = Block.objects.filter(block_type='custom')
        return form
