from django.views.generic.base import TemplateView
from django.db.models import Q, Count, Sum
from django_filters.views import FilterView
from django_tables2.views import (
    SingleTableMixin,
    MultiTableMixin
)

from django_tables2.paginators import LazyPaginator

from main import models, tables, filters
# Create your views here.

VISITORS_IP = 'VISITORS_IP'

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



class VisitorsTablesView(MultiTableMixin, TemplateView):
    template_name = "visitors.html"
    queryset = models.LogsLog.objects.filter(Q(name__header_name=VISITORS_IP)).values('value__header_value','value_id').annotate(visits = Count('value__header_value'))
    
    def __init__(self, *args, **kwargs):
        super(VisitorsTablesView, self).__init__(*args, **kwargs)
        print(dir(self.get_context_data))
    
    tables = [
        tables.VisitorTable(queryset,),
        tables.NetworkTable(queryset,exclude=("visits",))
    ]

    table_pagination = {
        "per_page": 10
    }



