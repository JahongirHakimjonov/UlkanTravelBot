from django.db import models

from apps.shared.models import AbstractBaseModel


class Order(AbstractBaseModel):
    tour = models.TextField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ("-created_at",)
