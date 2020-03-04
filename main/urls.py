from rest_framework import routers
from django.views.generic import TemplateView
from django.urls import path, include
from .endpoints import LogsLogViewSet
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django_filters.views import FilterView
from main import views
router = routers.DefaultRouter()
router.register(r'logslog', LogsLogViewSet)


urlpatterns = [
        path(
                '',
                views.VisitorsTablesView.as_view(),
        ),
        path(
                'visitors/',
                views.VisitorsTablesView.as_view(),
                name="visitors"
        ),
        path(
                'transactions/',
                views.FilteredTransactionsListView.as_view(template_name = "transactions.html"),
                name="transactions"
        ),
        path(
                'activity/',
                TemplateView.as_view(template_name="activity.html"),
                name="activity"
        ),
        path(
                'search/',
                TemplateView.as_view(template_name="search.html"),
                name="search"
        ),
        path(
                'all-notes/',
                TemplateView.as_view(template_name="all_notes.html"),
                name="all_notes"
        ),
        path(
                'tags/',
                TemplateView.as_view(template_name="tags.html"),
                name="tags"
        ),
        path(
                'login/',
                auth_views.LoginView.as_view(
                        template_name="login.html",
                ),
                name='login',
        ),
        path(
                'logout/',
                auth_views.LogoutView.as_view(
                        template_name="logout.html",
                ),
                name='logout',
        ),
        path('api/', include(router.urls)),
]