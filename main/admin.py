from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.HeaderName)
admin.site.register(models.HeaderValue)
admin.site.register(models.LogsTag)
admin.site.register(models.Transaction)
admin.site.register(models.LogsNote)
admin.site.register(models.TagCryteria)


