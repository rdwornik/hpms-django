from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from main import views

urlpatterns = [
    # path('', RedirectView.as_view(url='/hpms/login'), name='login_redirect'),
    path('hpms/admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('hpms/', include("main.urls")),
]
