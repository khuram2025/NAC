from django.db import models

class AVPolicy(models.Model):
    av_name = models.CharField(max_length=255)
    min_version = models.CharField(max_length=50)
    assigned_vlan = models.IntegerField()

    def __str__(self):
        return f"{self.av_name} v{self.min_version}+ -> VLAN {self.assigned_vlan}"

    class Meta:
        verbose_name_plural = "AV Policies"
        ordering = ['av_name', 'min_version']




class ClientHealth(models.Model):
    hostname = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=17, null=True, blank=True)
    av_status = models.BooleanField()
    av_name = models.CharField(max_length=255)
    av_version = models.CharField(max_length=50)
    av_up_to_date = models.BooleanField()
    assigned_vlan = models.IntegerField(null=True, blank=True)  # Add this line
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostname} - {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['hostname', 'timestamp']),
        ]