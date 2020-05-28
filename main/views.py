import datetime

from django.shortcuts import render
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
from dateutil.relativedelta import relativedelta
from main import utils
from django.db.models import Count, DateTimeField

#TODO cos przejscie z activity do transactions multiple tags ucinalo
#TODO Tags multiple header value 
#TODO wrzucic na azure
#TODO Godziny w activity 10:13 - 11:13
#TODO Przyciski w activity
#TODO testy
#TODO style kolumn wyrzucic
#TODO dodac paginacje dla visitors spytac sie o ilosc danych czy warrto robic pginacje dla tagow czy tez s    #TODO maybe make an agregation
#TODO maybe make an agregation instead of annotate perhaps


def all_notes_form_view(request,id=None,visitor_ip=None,transaction=None):
    if request.method == "GET":
        if not id:
            initial = {
                "visitor_ip" : visitor_ip,
                "transaction" : transaction
            }
            form = forms.NoteForm(initial=initial)
        else:
            try:
                note = models.LogsNote.objects.get(pk=id)
            except models.LogsNote.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            form = forms.NoteForm(instance=note)
        return render(request, "all_notes_form.html", { "form" : form })

    if request.method == "POST":
        if not id:
            initial = {
                "visitor_ip" : visitor_ip,
                "transaction" : transaction
            }
            note = models.LogsNote(**initial)
        else:
            try: 
                note = models.LogsNote.objects.get(pk=id)
            except models.LogsNote.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        form = forms.NoteForm(request.POST,instance=note)
        if form.has_changed() and form.is_valid():
            logsnote = form.save()
            if transaction:
                t = [models.Transaction.objects.get(pk=transaction)]
            else:   
                t = models.Transaction.objects.filter(Q(name__header_name=settings.VISITOR_IP) & Q(value__header_value=visitor_ip))
            logsnote.transactions.add(*t)
            return HttpResponseRedirect(reverse("all_notes"))
        return render(request, "all_notes_form.html", { "form" : form })

def all_notes_view(request):
    queryset = models.LogsNote.objects.all()

    if request.method == "POST"and request.POST.__contains__("selected_notes"):
            notes_to_delete = request.POST.getlist("selected_notes")
            queryset.objects.filter(id__in=notes_to_delete).delete()

    filter = filters.NoteFilter(request.GET,queryset=queryset)
    table = tables.NotesTable(filter.qs, order_by="-id") 
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, "all_notes.html",  {
        "form" : filter.form,
        "table": table
    })
    return render(request,"all_notes.html")

def activity_view(request):
    time_after =    datetime.datetime.fromisoformat(request.GET.get('time_after'))  if request.GET.get('time_after')    else (datetime.datetime.now() + relativedelta(years=-1))  
    time_before =   datetime.datetime.fromisoformat(request.GET.get('time_before')) if request.GET.get('time_before')   else datetime.datetime.now() 
    td = time_before - time_after       
    time_range = [key for key, value in utils.time_range.items() if value(td) == True][0]                                                
    trunc_func = utils.trunc_methods_table[time_range]
    qs = filters.ChartFilter(request.GET,queryset=models.Transaction.objects.all()).qs
    queryset = qs.annotate(date=trunc_func('time', output_field=DateTimeField())).values('date').order_by('date').annotate(visits_count=Count('pk'))
    current_date = utils.get_current_date[time_range](time_before)
    previous, next = utils.get_previous_and_next[time_range](time_after,time_before)
    print(previous)
    print(next)
    table = tables.ActivityTable(queryset,request=request,show_header=False)
    form = filters.ChartFilter(request.GET).form
    return render(request, "activity.html",  {
        "time_range": time_range,
        "current_date":current_date,
        "next" : next,
        "previous" : previous,
        "table" : table,
        "form" : form,
        "tag_field" : "assigned_tags",
    })

def transactions_detail_view(request, transaction=1,visitor_ip=1):
    t = models.Transaction.objects.get(pk=transaction)
    visitor_ip = t.logslog_set.filter(value=visitor_ip).first().value.header_value
    table = tables.TransactionsDetailTable(t.logslog_set.all())    
    return render(request, "transactions_detail.html", {
        "table":table,
        "transaction": transaction,
        "visitor_ip": visitor_ip
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
    initial = {"select":"search"}
    if request.method == "POST":
        if request.POST.get("select") == "delete_selected" \
        and request.POST.__contains__("selected_tags"):
            tags_to_delete = request.POST.getlist("selected_tags")
            models.LogsTag.objects.filter(id__in=tags_to_delete).delete()
        elif request.POST.get("select") == "search" and request.POST.get("tags"):
            queryset = models.LogsTag.objects.filter(tag__istartswith=request.POST.get("tags"))
            initial["tags"] = request.POST.get("tags")

    form = forms.TagsActionSelectForm(initial=initial)
    table = tables.TagsTable(queryset, order_by="-id") 
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, "tags.html",  {
        "form" : form,
        "table": table
    })

class FilteredTransactionsListView(SingleTableMixin, FilterView):
    table_class = tables.TransactionsTable
    filterset_class = filters.TransactionsFilter
    model = models.Transaction
    queryset = models.Transaction.objects.all()
    table_pagination = {
        "per_page": 10
    }
    def get(self, request, *args, **kwargs):
        filter = self.filterset_class(request.GET,queryset=self.get_queryset())
        table = self.table_class(filter.qs)    
        table.paginate(page=request.GET.get("page", 1), per_page=10, paginator_class=LazyPaginator)
        return render(request, "transactions.html",  {
            "form" : filter.form,
            "tag_field" : "assigned_tags",
            "table":table,
            "filter" : filter,
        })
            
class VisitorsTablesView(SingleTableView):
    template_name = "visitors.html"
    table_class = tables.VisitorTable
    queryset = models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITOR_IP)).values("header_value","id",visits=Count("id")) 
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }

