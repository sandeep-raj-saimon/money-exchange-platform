from django.contrib import admin
from .models import Provider

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'is_active')
    list_editable = ('priority', 'is_active')

admin.site.register(Provider, ProviderAdmin)
