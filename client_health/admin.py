from django.contrib import admin
from .models import ClientHealth, AVPolicy

@admin.register(ClientHealth)
class ClientHealthAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'av_status', 'av_name', 'av_version', 'av_up_to_date', 'assigned_vlan', 'timestamp')
    list_filter = ('av_status', 'av_name', 'av_up_to_date', 'assigned_vlan')
    search_fields = ('hostname', 'av_name')

@admin.register(AVPolicy)
class AVPolicyAdmin(admin.ModelAdmin):
    list_display = ('av_name', 'min_version', 'assigned_vlan')
    list_filter = ('av_name', 'assigned_vlan')
    search_fields = ('av_name', 'min_version')