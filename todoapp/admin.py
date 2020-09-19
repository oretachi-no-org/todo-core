from django.contrib import admin
from todoapp import models

admin.site.register(models.List)
admin.site.register(models.Task)
