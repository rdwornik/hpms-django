from rest_framework import routers
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from main import views
from .endpoints import LogsLogViewSet, ChartViewSet, VisitorIpList, LogsTagNameList, LogsNotesTitleList,LogsNotesVisitorIpList

router = routers.DefaultRouter(trailing_slash=True)
router.register(r"logslogs", LogsLogViewSet)
router.register(r"charts", ChartViewSet)
router.register(r"visitor-ip", VisitorIpList, basename="visitor-ip")
router.register(r"tag-names", LogsTagNameList, basename="tag-names")
router.register(r"note-titles", LogsNotesTitleList, basename="note-titles")
router.register(r"note-visitor-ip", LogsNotesVisitorIpList, basename="note-visitor-ip")

urlpatterns = [
        path(
                "",
                views.VisitorsTablesView.as_view(),
                name="home"
        ),
        path(
                "visitors/",
                views.VisitorsTablesView.as_view(),
                name="visitors"
        ),
        path(
                "transactions/",
                views.transactions_view,
                name="transactions"
        ),
        path(
                "transactions/<int:visitor_ip>/<int:transaction>/",
                views.transactions_detail_view,
                name="transactions_detail"
        ),
        path(
                "activity/",
                views.activity_view,
                name="activity"
        ),
        path(
                "search/",
                TemplateView.as_view(template_name="search.html"),
                name="search"
        ),
        path(
                "all-notes/",
                views.all_notes_view,
                name="all_notes"
        ),
        path(
                "all-notes/add/<str:visitor_ip>/",
                views.all_notes_form_view,
                name="all_notes_add"
        ),
        path(
                "all-notes/add/<str:visitor_ip>/<int:transaction>/",
                views.all_notes_form_view,
                name="all_notes_add"
        ),
        path(
                "all-notes/<int:id>/edit/",
                views.all_notes_form_view,
                name="all_notes_edit"
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
        path(
                "login/",
                auth_views.LoginView.as_view(template_name="login.html"),
                name="login",
        ),
        path(
                "logout/",
                auth_views.LogoutView.as_view(template_name="logout.html"),
                name="logout",
        ),
        path("api/", include(router.urls)),
]