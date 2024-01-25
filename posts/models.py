from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date = models.DateField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

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

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post/')

    def __str__(self):
        return self.image.name
