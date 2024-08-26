from django.contrib import admin
from .models import Switch, DeviceProfile, ManagedDevice

@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address')
    search_fields = ('name', 'ip_address')

@admin.register(DeviceProfile)
class DeviceProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'healthy_vlan', 'unhealthy_vlan')
    search_fields = ('name',)

@admin.register(ManagedDevice)
class ManagedDeviceAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'switch', 'port', 'profile', 'current_vlan', 'last_health_check')
    list_filter = ('switch', 'profile', 'current_vlan')
    search_fields = ('mac_address', 'port')