import django_tables2 as tables
from store.models import OrderItem

class OrderTable(tables.Table):
    class Meta:
        model = OrderItem
        template_name = "django_tables2/bootstrap.html"
        fields = ("order.id", "product.title", "price", "quantity")
