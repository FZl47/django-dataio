from django.contrib import admin

from . import models

admin.site.register(models.TestData)
admin.site.register(models.TestDataCat)