from django.shortcuts import render
import datetime
from django.db.models import Q, Count
from django_filters.views import FilterView
from django_tables2.views import (
    SingleTableMixin,
    SingleTableView
)
from django.conf import settings
from django_tables2.paginators import LazyPaginator
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse
from django.views.generic import View
from rest_framework import status
from main import models, tables, filters, forms
# Create your views here.
from dateutil.relativedelta import relativedelta
import datetime
from main import forms  

def activity_view(request):
    initial = { 'time_after' : (datetime.datetime.now() + relativedelta(years=-1)).strftime("%Y-%m-%d %H:%M") if request.GET.get('time_after') is None else datetime.datetime.fromisoformat(request.GET.get('time_after')).strftime("%Y-%m-%d %H:%M"),
                'time_before' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if request.GET.get('time_before') is None else datetime.datetime.fromisoformat(request.GET.get('time_before')).strftime("%Y-%m-%d %H:%M"),
                'assigned_tags' : request.GET.getlist('assigned_tags')}
    form = forms.TransactionBasicForm(initial)
    return render(request, "activity.html",  {
        "form" : form,
        "tag_field" : "assigned_tags",
    })

def transactions_detail_view(request, transaction=1):
    table = tables.TransactionsDetailTable(models.Transaction.objects.get(pk=transaction).logslog_set.all())    
    return render(request, "transactions_detail.html", {
        "table":table,
        "transaction": transaction
    })

def tags_form_view(request, id=None):
    if request.method == "GET":
        if not id:
            form = forms.TagForm()
        else:
            try:
                tag = models.LogsTag.objects.get(pk=id)
            except models.LogsTag.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            form = forms.TagForm(instance=tag)
        return render(request, "tags_form.html", { "form" : form })

    if request.method == "POST":
        if not id:
            tag = models.LogsTag()
            edited = False
        else:
            try:
                tag = models.LogsTag.objects.get(pk=id)
            except models.LogsTag.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            edited = True
        form = forms.TagForm(request.POST, instance=tag)
        if form.has_changed() and form.is_valid():
            tag = form.save()
            models.LogsTagAssign.objects.assign_tags_on_tags_created_or_updated(tag,edited)
            return HttpResponseRedirect(reverse("tags"))
        return render(request, "tags_form.html", { "form" : form })


def tags_view(request):
    queryset = models.LogsTag.objects.all()
    if request.method == "POST":
        if request.POST.get("select") == "delete_selected" \
        and request.POST.__contains__("selected_tags"):
            tags_to_delete = request.POST.getlist("selected_tags")
            models.LogsTag.objects.filter(id__in=tags_to_delete).delete()
        elif request.POST.get("select") == "search" and request.POST.get("tags"):
            queryset = models.LogsTag.objects.filter(tag__istartswith=request.POST.get("tags"))
    form = forms.TagsActionSelectForm(initial={"select":"search"})
    table = tables.TagsTable(queryset, order_by="-id") 
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, "tags.html",  {
        "form" : form,
        "table": table
    })

class FilteredTransactionsListView(SingleTableMixin, FilterView, FormView):
    table_class = tables.TransactionsTable
    filterset_class = filters.TransactionsFilter
    model = models.Transaction
    form_class = forms.TransactionsForm
    queryset = models.Transaction.objects.all()
    table_pagination = {
        "per_page": 10
    }
    def get(self, request, *args, **kwargs):
        initial = { 'time_after' : (datetime.datetime.now() + relativedelta(years=-1)).strftime("%Y-%m-%d %H:%M") if request.GET.get('time_after') is None else datetime.datetime.fromisoformat(request.GET.get('time_after')).strftime("%Y-%m-%d %H:%M"),
                    'time_before' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if request.GET.get('time_before') is None else datetime.datetime.fromisoformat(request.GET.get('time_before')).strftime("%Y-%m-%d %H:%M"),
                    'assigned_tags' : request.GET.getlist('assigned_tags')}
        form = self.form_class(initial)
        filter = self.filterset_class(request.GET,queryset=self.get_queryset())
        table = self.table_class(filter.qs)    
        table.paginate(page=request.GET.get("page", 1), per_page=10, paginator_class=LazyPaginator)
        return render(request, "transactions.html",  {
            "form" : form,
            "tag_field" : "assigned_tags",
            "table":table,
            "filter" : filter,
            "tag_field" : "assigned_tags",
        })
            
class VisitorsTablesView(SingleTableView):
    template_name = "visitors.html"
    table_class = tables.VisitorTable
    queryset = models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITORS_IP)).values("header_value","id",visits=Count("id")) 
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }

