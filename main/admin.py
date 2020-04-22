from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.LogsLog)
admin.site.register(models.HeaderName)
admin.site.register(models.HeaderValue)
admin.site.register(models.LogsTag)
admin.site.register(models.LogsTagAssign)
admin.site.register(models.Transaction)

