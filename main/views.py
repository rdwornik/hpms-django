from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q, Count, Sum
from django_filters.views import FilterView
from django_tables2.views import (
    SingleTableMixin,
    SingleTableView
)
from django.conf import settings
from django_tables2.paginators import LazyPaginator
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse
from dal import autocomplete
from main import models, tables, filters, forms, signals
# Create your views here.

def transactions_detail_view(request, transaction=1):
    table = tables.TransactionsDetailTable(models.LogsLog.objects.filter(Q(transaction = transaction)))    
    return render(request, "transactions_detail.html", {
        "table":table,
        "transaction": transaction
    })

def tags_form_view(request, id=None):
    if request.method == "GET":
        if not id:
            form = forms.TagForm()
        else:
            tag = models.LogsTag.objects.get(pk=id)
            form = forms.TagForm(instance=tag)
        return render(request, "tags_form.html", { "form" : form })

    if request.method == "POST":
        if not id:
            tag = models.LogsTag()
            edited = False
        else:
            tag = models.LogsTag.objects.get(pk=id)
            edited = True
        form = forms.TagForm(request.POST, instance=tag)
        if form.has_changed() and form.is_valid():
            tag = form.save()
            signals.tag_submited.send(sender=models.LogsTagAssign , tag=tag, edited=edited)
        return HttpResponseRedirect(reverse("tags"))

def tags_view(request):
    if request.method == "POST":
        if request.POST.get("select") == "delete_selected" \
        and request.POST.__contains__("selected_tags"):
            tags_to_delete = request.POST.getlist("selected_tags")
            models.LogsTag.objects.filter(id__in=tags_to_delete).delete()
    form = forms.TagsActionSelectForm(initial={"select":"empty"})
    table = tables.TagsTable(models.LogsTag.objects.all(), order_by="-id") 
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, "tags.html",  {
        "form" : form,
        "table": table
    })

class FilteredTagsListView(SingleTableMixin, FilterView, FormView):
    table_class = tables.TagsTable
    filterset_class = filters.TagsFilter
    form_class = forms.TagsActionSelectForm
    model = models.LogsTag
    queryset = models.LogsTag.objects.all()
    initial={"select":"empty"}
    table_pagination = {
        "per_page": 10
    }
    def post(self, request, *args, **kwargs):
        # super().post(request, *args, **kwargs)
        print(request.POST)
        if request.POST.get("select") == "delete_selected" \
        and request.POST.__contains__("selected_tags"):
            tags_to_delete = request.POST.getlist("selected_tags")
            models.LogsTag.objects.filter(id__in=tags_to_delete).delete()
        table = self.table_class(self.queryset, order_by="-id") 
        return render(request,self.template_name,{"form":self.form_class, "table":table,"filter":self.filterset_class})
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        table = self.table_class(self.queryset, order_by="-id") 
        return render(request,self.template_name,{"form":form, "table":table,"filter":self.filterset_class})

class FilteredTransactionsListView(SingleTableMixin, FilterView, FormView):
    table_class = tables.TransactionsTable
    filterset_class = filters.TransactionsFilter
    model = models.LogsLog
    queryset = models.LogsLog.objects.all()
    paginator_class = LazyPaginator
    form_class = forms.TransactionsAutocompleteForm
    table_pagination = {
        "per_page": 10
    }
    
class VisitorsTablesView(SingleTableView):
    template_name = "visitors.html"
    table_class = tables.VisitorTable
    queryset = models.LogsLog.objects.filter(Q(name__header_name=settings.VISITORS_IP)).values("value__header_value","value_id").annotate(visits = Count("value__header_value"))
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }

class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.LogsTag.objects.none()
        qs = models.LogsTag.objects.all()
        if self.q:
            qs = qs.filter(tag__istartswith=self.q)
        return qs

class VisitorsIPAutocompleteFromList(autocomplete.Select2ListView):
    def get_list(self):
        return  forms.get_choice_list()
    
    def autocomplete_results(self, results):
        return [(x,y) for x, y in results if self.q.lower() in x.lower()]
  
    def results(self, results):
        return [dict(id=id, text=value) for value, id in results]

        