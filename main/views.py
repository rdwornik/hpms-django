from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q, Count, Sum
from django_filters.views import FilterView
from django_tables2.views import (
    SingleTableMixin,
    SingleTableView
)

from django_tables2.paginators import LazyPaginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from main import models, tables, filters, forms
# Create your views here.

VISITORS_IP = 'VISITORS_IP'

def transaction_list(request, transaction=1):
    table = tables.TransactionTable(models.LogsLog.objects.filter(Q(transaction = transaction)))    
    return render(request, "transactions_detail.html", {
        "table":table,
        "transaction": transaction
    })

def action_tag(request, id=None):
    if request.method == "GET":
        if not id:
            form = forms.TagForm()
        else:
            tag = models.LogsTag.objects.get(pk=id)
            form = forms.TagForm(instance=tag)
            # form.is_valid()
            # form.save()
    if request.method == "POST":
        if not id:
            form = forms.TagForm()
        else:
            tag = models.LogsTag.objects.get(pk=id)
            form = forms.TagForm(request.POST, instance=tag)
            form.save()
            return HttpResponseRedirect(reverse('tags'))
    return render(
        request,
        "tags_action.html",
        {
            'form':form
        }
    )


def tags_form(request):
    action = forms.TagsActionSelectForm(initial={'select':'empty'})
    table = tables.TagsTable(models.LogsTag.objects.all())
    return render(request, "tags.html",  {
        'action' : action,
        'table': table
    })

class FilteredTransactionsListView(SingleTableMixin, FilterView):
    table_class = tables.TransactionsTable
    filterset_class = filters.TransactionsFilter
    model = models.LogsLog
    queryset = models.LogsLog.objects.all()
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }
class VisitorsTablesView(SingleTableView):
    template_name = "visitors.html"
    table_class = tables.VisitorTable
    queryset = models.LogsLog.objects.filter(Q(name__header_name=VISITORS_IP)).values('value__header_value','value_id').annotate(visits = Count('value__header_value'))
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }
