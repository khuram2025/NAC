# pc_health_monitor/urls.py
from django.contrib import admin
from django.urls import path
from client_health.views import update_client_health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('update/', update_client_health, name='update_client_health'),
]