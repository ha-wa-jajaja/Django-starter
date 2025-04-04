from django.contrib import admin

from .models import Order, OrderItem, Product

# Register your models here.


# NOTE:
# Admin.TabularInline allows to edit related objects
# in a tabular format directly within the admin page of their parent object.
# (Also has StackedInline for a different layout)
class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    # NOTE:
    # Inlines in admin.ModelAdmin allows to edit related objects directly on the same page
    # as the parent object in the Django admin interface.
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
