from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/hpms3/login'), name='login_redirect'),
    path('hpms3/admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('hpms3/', include("main.urls")),
]
