from rest_framework import routers
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django_filters.views import FilterView

from main import views
from .endpoints import LogsLogViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register(r"logslogs", LogsLogViewSet)


urlpatterns = [
        path(
                "",
                views.VisitorsTablesView.as_view(),
        ),
        path(
                "visitors/",
                views.VisitorsTablesView.as_view(),
                name="visitors"
        ),
        path(
                "transactions/",
                views.FilteredTransactionsListView.as_view(template_name = "transactions.html"),
                name="transactions"
        ),
        path(
                "transactions/<int:transaction>/",
                views.transactions_detail_view,
                name="transactions_detail"
        ),
        path(
                "activity/",
                TemplateView.as_view(template_name="activity.html"),
                name="activity"
        ),
        path(
                "search/",
                TemplateView.as_view(template_name="search.html"),
                name="search"
        ),
        path(
                "all-notes/",
                TemplateView.as_view(template_name="all_notes.html"),
                name="all_notes"
        ),
        path(
                "tags/add/",
                views.tags_form_view,
                name="tags_add"
        ),
        path(
                "tags/<int:id>/edit/",
                views.tags_form_view,
                name="tags_edit"
        ),
        path(
                "tags/",
                views.tags_view,
                name="tags"
        ),
        url(
                r'^tags-autocomplete/$',
                views.TagsAutocomplete.as_view(),
                name='tags-autocomplete',
        ),
        path(
                "login/",
                auth_views.LoginView.as_view(
                        template_name="login.html",
                ),
                name="login",
        ),
        path(
                "logout/",
                auth_views.LogoutView.as_view(
                        template_name="logout.html",
                ),
                name="logout",
        ),
        path("api/", include(router.urls)),
]