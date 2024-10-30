from django.db import models

from apps.shared.models import AbstractBaseModel


class Group(AbstractBaseModel):
    name = models.CharField(max_length=255)
    group_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ("-created_at",)
