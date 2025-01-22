from django.db import models
from django.db.models import Count, Sum, F
from django.utils.timezone import now, timedelta
from django.db.models.functions import Coalesce


# Models
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.name

    # Add any custom methods that were previously in the manager
    def with_order_count(self):
        return self.annotate(order_count=Count('orders'))

    def with_total_spent(self):
        return self.annotate(
            total_spent=Coalesce(
                Sum(
                    F('orders__order_items__product__price') * F('orders__order_items__quantity')
                ), 
                0
            )
        )

    def frequent_customers(self, min_orders=2):
        return self.with_order_count().filter(order_count__gte=min_orders)


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    # Custom method for expensive products
    def expensive_products(self, min_price=100):
        return self.filter(price__gte=min_price)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"

    # Custom method for recent orders
    def recent_orders(self, days=7):
        date_threshold = now() - timedelta(days=days)
        return self.filter(order_date__gte=date_threshold)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    # Custom method for total quantity
    def total_quantity(self):
        return self.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
