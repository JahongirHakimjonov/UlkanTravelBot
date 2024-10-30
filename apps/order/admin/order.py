from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.order.models import Order


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email", "phone")

