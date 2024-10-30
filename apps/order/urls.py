from django.urls import path

from apps.order.views import OrderCreateView

urlpatterns = [
    path("order/", OrderCreateView.as_view(), name="order"),
]
