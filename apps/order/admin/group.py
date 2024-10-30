from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.order.models import Group


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ("name", "group_id")
    search_fields = ("name", "group_id")
