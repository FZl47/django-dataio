from django.db import models

from django_dataio.mixins import DjangoDataIOModelMixin


class TestDataCat(DjangoDataIOModelMixin, models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TestData(DjangoDataIOModelMixin, models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    number = models.IntegerField(default=10)
    category = models.ForeignKey('TestDataCat', on_delete=models.CASCADE, null=True, blank=True)
