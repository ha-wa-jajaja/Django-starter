import uuid
from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    # image = models.ImageField(upload_to='products/', blank=True, null=True)

    # NOTE: @property is a py built in decorator to allow getting computed value without ()
    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    # NOTE: models.TextChoices acts as ENUM
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    # NOTE:
    # through= :Instead of letting Django create junction table, specify to manage relationship 
    # through OrderItem class, useful when want to add additional field such as quantity
    # related_name= : Creates a reverse relationship from self to related table. 
    # Here allows access all orders that contain a specific product by using product.orders.all().
    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders')

    def __str__(self):
        return f"Order {self.order_id }"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,         related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"