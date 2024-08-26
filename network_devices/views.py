from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import ClientHealth
from network_devices.models import ManagedDevice, DeviceProfile
from django.utils import timezone

@csrf_exempt
@require_POST
def update_client_health(request):
    try:
        data = json.loads(request.body)
        client_health = ClientHealth(
            hostname=data['hostname'],
            av_status=data['status'],
            av_name=data['name'],
            av_version=data['version'],
            av_up_to_date=data['up_to_date']
        )
        client_health.save()

        # Device profiling and VLAN assignment
        mac_address = data.get('mac_address')
        if mac_address:
            managed_device = ManagedDevice.objects.filter(mac_address=mac_address).first()
            if managed_device:
                profile = managed_device.profile
                if profile:
                    new_vlan = profile.healthy_vlan if client_health.av_status and client_health.av_up_to_date else profile.unhealthy_vlan
                    if new_vlan != managed_device.current_vlan:
                        # TODO: Implement VLAN change on the switch
                        managed_device.current_vlan = new_vlan
                        managed_device.save()

                managed_device.last_health_check = timezone.now()
                managed_device.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)