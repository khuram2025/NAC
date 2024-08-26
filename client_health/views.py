from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import ClientHealth, AVPolicy
from network_devices.models import ManagedDevice
from .utils import compare_versions
from .network_utils import change_device_vlan
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def update_client_health(request):
    try:
        data = json.loads(request.body)
        print(f"Received data: {data}")
        
        # Find the appropriate policy
        policies = AVPolicy.objects.filter(av_name__iexact=data['name']).order_by('-min_version')
        print(f"Found {policies.count()} matching policies for {data['name']}")
        
        assigned_vlan = None
        
        for policy in policies:
            print(f"Checking policy: {policy.av_name}, min_version: {policy.min_version}, client version: {data['version']}")
            comparison_result = compare_versions(data['version'], policy.min_version)
            print(f"Version comparison result: {comparison_result}")
            if comparison_result >= 0:
                assigned_vlan = policy.assigned_vlan
                print(f"Matched policy, assigned VLAN: {assigned_vlan}")
                break
        
        # If no matching policy found, you might want to assign a default VLAN
        if assigned_vlan is None:
            assigned_vlan = 999  # Replace with your default VLAN
            print(f"No matching policy found, using default VLAN: {assigned_vlan}")

        client_health = ClientHealth(
            hostname=data['hostname'],
            mac_address=data.get('mac_address'),
            av_status=data['status'],
            av_name=data['name'],
            av_version=data['version'],
            av_up_to_date=data['up_to_date'],
            assigned_vlan=assigned_vlan
        )
        client_health.save()
        print(f"Saved ClientHealth record: {client_health}")

        # Attempt to change the device's VLAN
        managed_device = ManagedDevice.objects.filter(mac_address=data.get('mac_address')).first()
        if managed_device:
            change_vlan_result = change_device_vlan(managed_device, assigned_vlan)
        else:
            change_vlan_result = f"No managed device found for MAC address: {data.get('mac_address')}"
        print(f"VLAN change result: {change_vlan_result}")

        return JsonResponse({
            'status': 'success',
            'assigned_vlan': assigned_vlan,
            'vlan_change_result': change_vlan_result
        })
    except Exception as e:
        print(f"Error in update_client_health: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
def change_device_vlan(managed_device, new_vlan):
    switch = managed_device.switch
    device = {
        'device_type': 'cisco_ios',  # Adjust if you're using a different switch type
        'ip': switch.ip_address,
        'username': switch.username,
        'password': switch.password,
        'secret': switch.password,  # Assuming enable password is the same as login password
    }

    try:
        with ConnectHandler(**device) as conn:
            commands = [
                f'interface {managed_device.port}',
                f'switchport access vlan {new_vlan}',
                'exit'
            ]
            output = conn.send_config_set(commands)
            logger.info(f"Changed VLAN for {managed_device.mac_address} to {new_vlan} on port {managed_device.port}")
            return f"VLAN changed to {new_vlan} for {managed_device.mac_address} on port {managed_device.port}"
    except Exception as e:
        logger.exception(f"Error changing VLAN for {managed_device.mac_address}")
        return f"Error changing VLAN: {str(e)}"