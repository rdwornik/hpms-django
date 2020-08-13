from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html")),
    path('hpms3/', RedirectView.as_view(url='/hpms3/login'), name='login_redirect'),
    path('hpms3/admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('hpms3/', include("main.urls")),
]