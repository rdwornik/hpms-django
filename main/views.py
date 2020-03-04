from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from django_tables2.views import (
    SingleTableMixin,
    MultiTableMixin
)

from main import models, tables, filters
# Create your views here.

class FilteredTransactionsListView(SingleTableMixin, FilterView):
    table_class = tables.TransactionsTable
    filterset_class = filters.TransactionsFilter
    model = models.LogsLog
    queryset = models.LogsLog.objects.distinct('transaction')
    # table_data =  models.LogsLog.objects.distinct('transaction')

class VisitorsTablesView(MultiTableMixin, TemplateView):
    template_name = "visitors.html"
    qs = models.LogsLog.objects.all()

    tables = [
        tables.VisitorTable(qs,),
        tables.NetworkTable(qs)
    ]

    # table_pagination = {
    #     "per_page": 10
    # }



