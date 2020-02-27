from rest_framework import routers
from django.urls import path, include
from .endpoints import LogsLogViewSet


router = routers.DefaultRouter()
router.register(r'logslog', LogsLogViewSet)


urlpatterns = [
        path('api/', include(router.urls)),
]