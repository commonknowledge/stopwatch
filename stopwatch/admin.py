from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from stopwatch import models


@admin.register(models.StopWatchDocument, models.StopwatchImage)
class GenericAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    pass
