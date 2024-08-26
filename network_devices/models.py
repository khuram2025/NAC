from django.db import models

class Switch(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Consider using encrypted fields for production

    def __str__(self):
        return self.name

class DeviceProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    healthy_vlan = models.IntegerField()
    unhealthy_vlan = models.IntegerField()

    def __str__(self):
        return self.name

class ManagedDevice(models.Model):
    mac_address = models.CharField(max_length=17, unique=True)
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
    port = models.CharField(max_length=50)
    profile = models.ForeignKey(DeviceProfile, on_delete=models.SET_NULL, null=True)
    current_vlan = models.IntegerField()
    last_health_check = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.mac_address} on {self.switch.name} port {self.port}"