from django.contrib import admin

import timetracker.models as models

admin.site.register(models.UserData)
admin.site.register(models.Span)
admin.site.register(models.Task)
