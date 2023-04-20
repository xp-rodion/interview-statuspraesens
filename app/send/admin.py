from django.contrib import admin

from . import models


@admin.register(models.Email)
class MailingAdmin(admin.ModelAdmin):
    model = models.Email
    list_display = (
    'uid', 'receiver', 'receiver_copy', 'title', 'body', 'created', 'modified', 'departure_date', 'result')
    ordering = ('modified',)
    readonly_fields = ('uid',)
