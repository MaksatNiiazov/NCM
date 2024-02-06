from modeltranslation.translator import register, TranslationOptions

from posts.models import Category, Tag, Post
from .models import TextBlock, Slide, SliderBlock, TextWithImageBlock, CardsBlock, Card, Header, \
    CustomHTMLBlock, TextSliderBlock, BaseDirection, Footer, Page


@register(Post)
class PostranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(TextBlock)
class TextBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(SliderBlock)
class SliderBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(BaseDirection)
class BaseDirectionTranslationOptions(TranslationOptions):
    pass


@register(TextWithImageBlock)
class TextWithImageBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(Card)
class CardTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(CardsBlock)
class CardsBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(TextSliderBlock)
class TextSliderBlockTranslationOptions(TranslationOptions):
    pass


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Footer)
class FooterTranslationOptions(TranslationOptions):
    fields = ('about_us',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)
