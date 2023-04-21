from django.contrib import admin

from validate_email.models import EmailResult, EmailFile


@admin.register(EmailFile)
class EmailFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at')
    ordering = ('created_at', )


@admin.register(EmailResult)
class EmailResultAdmin(admin.ModelAdmin):
    list_display = ('file', 'email', 'is_valid')

