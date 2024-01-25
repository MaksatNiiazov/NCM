from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from posts.models import Post


class Header(models.Model):
    is_default = models.BooleanField(default=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    background_image = models.ImageField(upload_to='headers/', blank=True, null=True)
    height = models.PositiveIntegerField(default=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    logo_alt_text = models.CharField(max_length=100, default='Logo')
    logo_width = models.PositiveIntegerField(default=75)
    logo_height = models.PositiveIntegerField(default=75)
    title_color = models.CharField(max_length=7, default='#FFFFFF')
    subtitle_color = models.CharField(max_length=7, default='#FFFFFF')
    background_color = models.CharField(max_length=7, default='#000000')
    menu_items = models.ManyToManyField('Page', related_name='headers')

    def __str__(self):
        return self.title if self.title else "Header for Page: {}".format(self.page.title)


class Footer(models.Model):
    is_default = models.BooleanField(default=False)
    about_us = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    copyright_text = models.CharField(max_length=200)
    background_color = models.CharField(max_length=7, default='#FFFFFF')
    text_color = models.CharField(max_length=7, default='#000000')
    link_color = models.CharField(max_length=7, default='#007bff')
    order = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ['order']


class SocialLinks(models.Model):
    footer = models.ForeignKey(Footer, on_delete=models.DO_NOTHING)
    icon = models.ImageField(upload_to='footer/icons', blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    social_links = models.CharField(max_length=200, blank=True, null=True)
    link_color = models.CharField(max_length=7, default='#007bff')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    main_page = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    header = models.ForeignKey(Header, on_delete=models.DO_NOTHING)
    footer = models.ForeignKey(Footer, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.create_unique_slug()
        super().save(*args, **kwargs)

    def create_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

class BaseModel(models.Model):
    border_radius = models.PositiveIntegerField(default=5)
    padding = models.CharField(max_length=50, default='50')
    margin = models.CharField(max_length=50, default='0 auto')
    background_color = models.CharField(max_length=15, default='#ffffff')
    title = models.CharField(max_length=100, blank=True, null=True)
    title_size = models.PositiveIntegerField(default=36)
    title_color = models.CharField(max_length=7, default='#000000')
    text = models.TextField(blank=True, null=True)
    text_size = models.PositiveIntegerField(default=18)
    text_color = models.CharField(max_length=7, default='#000000')

    class Meta:
        abstract = True


class BaseDirection(BaseModel):
    LEFT = 'L'
    RIGHT = 'R'

    DIRECTION_CHOICES = [
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
    ]
    direction = models.CharField(
        max_length=1,
        choices=DIRECTION_CHOICES,
        default=LEFT,
    )


class Block(models.Model):
    CHOICES = [
        ('text', 'Text'),
        ('text_image', 'Text Image'),
        ('slider', 'Slider'),
        ('cards', 'Cards'),
        ('custom', 'Custom'),
        ('text_slider', 'Text Slider')
    ]
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    block_type = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='text',
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.page} || {self.title}'


class TextBlock(BaseModel):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, related_name='text_block')


class TextWithImageBlock(BaseDirection):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, related_name='text_image_block')
    image = models.ImageField(upload_to='images/')
    image_width = models.PositiveIntegerField(default=300, help_text="Enter the width of the image in pixels")
    image_height = models.PositiveIntegerField(default=300, help_text="Enter the height of the image in pixels")
    alt = models.CharField(max_length=100, blank=True, null=True, default='Image')


class SliderBlock(BaseModel):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, related_name='slider')
    slides_per_view_desktop = models.PositiveIntegerField(default=5)
    slides_per_view_tablet = models.PositiveIntegerField(default=3)
    slides_per_view_mobile = models.PositiveIntegerField(default=1)
    navigation_color = models.CharField(max_length=15, default='blue')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Slide(models.Model):
    slider_block = models.ForeignKey(SliderBlock, on_delete=models.CASCADE, related_name='slides')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    width = models.PositiveIntegerField(default=300)
    height = models.PositiveIntegerField(default=300)
    image = models.ImageField(upload_to='slides/')
    alt = models.CharField(max_length=100, blank=True, null=True, default='Image')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class TextSliderBlock(SliderBlock):
    LEFT = 'L'
    RIGHT = 'R'

    DIRECTION_CHOICES = [
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
    ]
    direction = models.CharField(
        max_length=1,
        choices=DIRECTION_CHOICES,
        default=LEFT,
    )


class CardsBlock(BaseModel):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, related_name='cards_block')
    cards_per_row_desktop = models.PositiveIntegerField(default=4)
    cards_per_row_tablet = models.PositiveIntegerField(default=3)
    cards_per_row_mobile = models.PositiveIntegerField(default=2)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Card(models.Model):
    cards_block = models.ForeignKey(CardsBlock, on_delete=models.CASCADE, related_name='cards')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='cards/')
    width = models.PositiveIntegerField(default=100)
    height = models.PositiveIntegerField(default=100)
    text = models.CharField(max_length=150, blank=True, null=True)
    text_color = models.CharField(max_length=7, default='#000000')
    alt = models.CharField(max_length=100, blank=True, null=True, default='Image')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class CustomHTMLBlock(BaseModel):
    block = models.OneToOneField(Block, on_delete=models.CASCADE, related_name='custom_block')
    name = models.CharField(max_length=100, help_text="A unique name for this HTML block.")
    html_content = models.TextField(help_text="The HTML content to be inserted.")

    def display_html(self):
        return mark_safe(self.html_content)

    def __str__(self):
        return self.name
