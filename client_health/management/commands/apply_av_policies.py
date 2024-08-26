from django.core.management.base import BaseCommand
from client_health.models import ClientHealth, AVPolicy
from client_health.utils import compare_versions
from client_health.network_utils import change_device_vlan

class Command(BaseCommand):
    help = 'Apply AV policies to all clients and update VLANs if necessary'

    def handle(self, *args, **options):
        clients = ClientHealth.objects.all()
        for client in clients:
            policies = AVPolicy.objects.filter(av_name__iexact=client.av_name).order_by('-min_version')
            new_vlan = None

            for policy in policies:
                if compare_versions(client.av_version, policy.min_version) >= 0:
                    new_vlan = policy.assigned_vlan
                    break

            if new_vlan is None:
                new_vlan = 999  # Replace with your default VLAN

            if new_vlan != client.assigned_vlan:
                client.assigned_vlan = new_vlan
                client.save()
                result = change_device_vlan(client.hostname, new_vlan)
                self.stdout.write(self.style.SUCCESS(f'Updated VLAN for {client.hostname}: {result}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'No VLAN change needed for {client.hostname}'))