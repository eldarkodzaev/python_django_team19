from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from app_users.models import User
from .utils import product_directory_path


class Category(MPTTModel):
    """Модель категорий товара"""
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_min_price(self):
        return min(Product.objects.filter(category=self).values_list('price', flat=True))

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, verbose_name='category')
    description = models.CharField(max_length=1000, verbose_name='description')
    is_limited = models.BooleanField(default=False, verbose_name='is limited')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    quantity = models.PositiveIntegerField(default=0, verbose_name='quantity')
    image = models.ImageField(upload_to=product_directory_path, blank=True, null=True,
                              verbose_name='image')  # основное фото
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    free_delivery = models.BooleanField(default=False, verbose_name='free delivery')
    sales_count = models.PositiveIntegerField(default=0, verbose_name='sales count')
    tags = TaggableManager(verbose_name='tags')

    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product:product', args=[self.slug])


class Image(models.Model):
    """Модель фотографии товара"""
    image = models.ImageField(upload_to=product_directory_path, blank=True, null=True, verbose_name='image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='product')

    class Meta:
        db_table = 'image'
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.product.name


class Review(models.Model):
    """Модель отзыва"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='product')
    text = models.TextField(verbose_name='text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')

    class Meta:
        db_table = 'review'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return f"Review for {self.product} by {self.user}"
