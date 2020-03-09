from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q, Count, Sum
from django_filters.views import FilterView
from django_tables2.views import (
    SingleTableMixin,
    SingleTableView
)

from django_tables2.paginators import LazyPaginator

from main import models, tables, filters
# Create your views here.

VISITORS_IP = 'VISITORS_IP'

def transaction_list(request, transaction=1):
    table = tables.TransactionTable(models.LogsLog.objects.filter(Q(transaction = transaction)))    
    return render(request, "transactions_detail.html", {
        "table":table,
        "transaction": transaction
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
    # table_data =  models.LogsLog.objects.distinct('transaction')

class VisitorsTablesView(SingleTableView):
    template_name = "visitors.html"
    table_class = tables.VisitorTable
    queryset = models.LogsLog.objects.filter(Q(name__header_name=VISITORS_IP)).values('value__header_value','value_id').annotate(visits = Count('value__header_value'))
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }
