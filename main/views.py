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

#TODO wyminic select2 na jquery
#TODO zrobic multiple ip
#TODO cos przejscie z activity do transactions multiple tags ucinalo
#TODO wrzucic na azure
#TODO zmienic model transactions
#TODO Godziny w activity 10:13 - 11:13
#TODO Przyciski w activity
#TODO multiple tags
#TODO testy
#TODO style kolumn wyrzucic
#TODO dodac paginacje dla visitors spytac sie o ilosc danych czy warrto robic pginacje dla tagow czy tez serwera


def all_notes_form_view(request,id=None,ip=None,transaction=None):
    if request.method == "GET":
        if not id:
            initial = {
                "ip" : models.HeaderValue.objects.get(pk=ip),
                "transaction" : models.Transaction.objects.get(pk=transaction)  if transaction else models.Transaction()
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
                "ip" : models.HeaderValue.objects.get(pk=ip),
                "transaction" : models.Transaction.objects.get(pk=transaction)  if transaction else models.Transaction()
            }
            note = models.LogsNote(title=request.POST['title'],content=request.POST['content'],transaction=initial['transaction'],ip=initial['ip'])
        else:
            try:
                initial = {}
                note = models.LogsNote.objects.get(pk=id)
            except models.LogsNote.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        initial['title'] = request.POST["title"]
        initial['content'] = request.POST['content']
        form = forms.NoteForm(initial,instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("all_notes"))
        return render(request, "all_notes_form.html", { "form" : form })

def all_notes_view(request):
    queryset = models.LogsNote.objects.all()
    initial = {"select":"search"}
    if request.method == "POST":
        if request.POST.get("select") == "delete_selected" \
        and request.POST.__contains__("selected_notes"):
            notes_to_delete = request.POST.getlist("selected_notes")
            models.LogsNote.objects.filter(id__in=notes_to_delete).delete()
        elif request.POST.get("select") == "search" and request.POST.get("title"):
            queryset = models.LogsNote.objects.filter(title__istartswith=request.POST.get("title"))
            initial["title"] = request.POST.get("title")
    
    form = forms.NotesActionSelectForm(initial=initial)
    table = tables.NotesTable(queryset, order_by="-id") 
    table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, "all_notes.html",  {
        "form" : form,
        "table": table
    })

def activity_view(request):
    # initial = { 'time_after' : (datetime.datetime.now() + relativedelta(years=-1)).strftime("%Y-%m-%d %H:%M") if request.GET.get('time_after') is None else datetime.datetime.fromisoformat(request.GET.get('time_after')).strftime("%Y-%m-%d %H:%M"),
    #             'time_before' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if request.GET.get('time_before') is None else datetime.datetime.fromisoformat(request.GET.get('time_before')).strftime("%Y-%m-%d %H:%M"),
    #             'assigned_tags' : request.GET.getlist('assigned_tags')}
    form = filters.ChartFilter(request.GET).form
    return render(request, "activity.html",  {
        "form" : form,
        "tag_field" : "assigned_tags",
    })

def transactions_detail_view(request, transaction=1,ip=1):
    table = tables.TransactionsDetailTable(models.Transaction.objects.get(pk=transaction).logslog_set.all())    
    return render(request, "transactions_detail.html", {
        "table":table,
        "transaction": transaction,
        "ip": ip
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
    queryset =  models.Transaction.objects.values("visitor_ip").order_by().annotate(visits=Count("visitor_ip"))
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }

