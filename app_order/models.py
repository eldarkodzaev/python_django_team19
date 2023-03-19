from django.db import models

from app_cart.models import Cart
from app_goods.models import Product
from app_users.models import User


class Order(models.Model):
    """Модель заказа"""
    DELIVERY_TYPES = [
        ('regular', 'обычная доставка'),
        ('express', 'экспресс-доставка')
    ]
    PAYMENT_TYPES = [
        ('card', 'онлайн картой'),
        ('random', 'онлайн со случайного чужого счета')
    ]

    STATUS_CREATED = 'created'
    STATUS_OK = 'ok'
    STATUS_DELIVERED = 'delivered'
    STATUS_PAID = 'paid'
    STATUS_NOT_PAID = 'not paid'
    STATUS_CHOICES = [
        ('Success', (
            (STATUS_CREATED, 'создан'),
            (STATUS_OK, 'выполнен'),
            (STATUS_DELIVERED, 'доставляется'),
            (STATUS_PAID, 'оплачен'),
        )
         ),
        (STATUS_NOT_PAID, 'не оплачен'),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    delivery_type = models.CharField(max_length=15, choices=DELIVERY_TYPES, verbose_name='delivery type')
    city = models.CharField(max_length=50, verbose_name='city')
    address = models.CharField(max_length=255, verbose_name='address')
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPES, verbose_name='payment type')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='status')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='user')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='cart')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='total price')

    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f"Order #{self.pk} by {self.user}"

