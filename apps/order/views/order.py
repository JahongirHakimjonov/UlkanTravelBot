from rest_framework import generics
from apps.order.models import Order
from apps.order.serializers.order import OrderSerializer

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer