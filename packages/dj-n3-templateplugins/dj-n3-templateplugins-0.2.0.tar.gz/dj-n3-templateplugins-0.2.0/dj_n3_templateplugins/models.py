# -*- coding: utf-8 -*-
from django.db import models
from django_extensions.db.models import TimeStampedModel


STATUS_CHOICES = {
    (0, 'ENABLED'),
    (1, 'DISABLED'),
}


class Plugin(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    pythonpath = models.CharField(max_length=128, unique=True)
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


