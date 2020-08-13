import datetime

from django.shortcuts import render
from django.db.models import Q, Count, DateTimeField, OuterRef, Subquery
from django_tables2.views import SingleTableView
from django_tables2 import RequestConfig
from django_tables2.paginators import LazyPaginator
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404

from main import models, tables, filters, forms, utils

class VisitorsTablesView(SingleTableView):
    template_name = "visitors.html"
    table_class = tables.VisitorTable
    queryset = models.HeaderValue.objects.filter(Q(header_names__header_name=settings.VISITOR_IP)).values("header_value","id",visits=Count("id")) 
    paginator_class = LazyPaginator
    table_pagination = {
        "per_page": 10
    }
    
def transactions_view(request):

    if request.GET.get("action") == "delete":
        visitors_to_delete = request.GET.getlist("visitor_ip")
        models.Transaction.objects.filter(value__in=visitors_to_delete).delete()
    
    if request.GET.get("action") == "addnote":
        visitor_ip = request.GET.get("visitor_ip")
        value = models.HeaderValue.objects.get(pk=visitor_ip).header_value
        reverse("all_notes_add",kwargs={"visitor_ip":value})
        return JsonResponse({'url':reverse("all_notes_add",kwargs={"visitor_ip":value})})

    filter = filters.TransactionsFilter(request.GET,queryset=models.Transaction.objects.all())
    subquery = filter.qs.filter(Q(transaction=OuterRef('transaction')) & 
                                    (Q(name__header_name=settings.SERVER_NAME) | 
                                    Q(name__header_name=settings.VISITOR_IP)  | 
                                    Q(name__header_name=settings.REQUEST_URI))).order_by('transaction')
    
    queryset = filter.qs.annotate(server=Subquery(subquery.filter(Q(name__header_name=settings.SERVER_NAME)).values('value__header_value')[:1]),
                                                    visitor_ip=Subquery(subquery.filter(Q(name__header_name=settings.VISITOR_IP)).values('value__header_value')[:1]),
                                                    request_uri=Subquery(subquery.filter(Q(name__header_name=settings.REQUEST_URI)).values('value__header_value')[:1]))
    table = tables.TransactionsTable(queryset)
    RequestConfig(request,paginate={"per_page": 10,"paginator_class":LazyPaginator}).configure(table)
    return render(request, "transactions.html",  {
        "form" : filter.form,
        "tag_field" : "assigned_tags",
        "table":table,
        "filter" : filter,
    })

def transactions_detail_view(request,visitor_ip, transaction=1,delete=None):
    if delete:
        models.Transaction.objects.get(pk=transaction).delete()
        return HttpResponseRedirect(reverse("transactions"))

    t = models.Transaction.objects.get(pk=transaction)
    table = tables.TransactionsDetailTable(t.logslog_set.all())    
    RequestConfig(request,paginate={"per_page": 25}).configure(table)
    return render(request, "transactions_detail.html", {
        "table":table,
        "transaction": transaction,
        "visitor_ip": visitor_ip
    })

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
    
def tags_form_view(request, id=None):
    #Create a form
    if not id:
        tag = models.LogsTag()
        queryset = models.TagCryteria.objects.none()
        edited=False
    else:
        tag = get_object_or_404(models.LogsTag,pk=id)
        queryset = tag.cryterias.all()
        edited=True
    #Post form
    if request.method == "POST":
        form = forms.LogsTagForm(request.POST, instance=tag)
        formset = forms.TagCryteriaFormSet(
            request.POST,
            queryset=queryset
        )
        if form.is_valid() and form.has_changed() and formset.is_valid():
            tag = form.save()

        if formset.is_valid() and formset.has_changed():
            instances = formset.save(commit=False)
            for new in formset.new_objects:
                cryteria, created = models.TagCryteria.objects.get_or_create(name_cryteria=new.name_cryteria,value_cryteria=new.value_cryteria)
                tag.cryterias.add(cryteria)

            for changed_obj, changed_data in formset.changed_objects:
                old_cryteria = queryset.get(pk=changed_obj.pk)
                if old_cryteria.logstag_set.count() == 1:
                    old_cryteria.delete()
                else:
                    tag.cryterias.remove(old_cryteria)
                cryteria, created = models.TagCryteria.objects.get_or_create(name_cryteria=changed_obj.name_cryteria,value_cryteria=changed_obj.value_cryteria)
                tag.cryterias.add(cryteria)

            for to_delete in formset.deleted_objects:
                old_cryteria = queryset.get(pk=to_delete.pk)
                if old_cryteria.logstag_set.count() == 1:
                    old_cryteria.delete()
                else:
                    tag.cryterias.remove(old_cryteria)
                if tag.cryterias.count() == 0:
                    tag.delete()
                    return HttpResponseRedirect(reverse("tags"))

            models.LogsTagAssign.objects.assign_tags_on_tags_created(tag,edited)
            return HttpResponseRedirect(reverse("tags"))
        return render(request, "tags_form.html",{"formset":formset,"form":form})

    form = forms.LogsTagForm(instance=tag)
    formset = forms.TagCryteriaFormSet(queryset=queryset) 
    return render(request, "tags_form.html",{"formset":formset,"form":form})

def tags_view(request):
    queryset = models.LogsTag.objects.all()
    if request.method == "POST"and request.POST.__contains__("selected_tags"):
        selected_tags = request.POST.getlist("selected_tags")
        tags_to_delete = models.LogsTag.objects.filter(id__in=selected_tags)
        for tag_to_delete in tags_to_delete:
            for cryteria in tag_to_delete.cryterias.all():
                if cryteria.logstag_set.count() == 1:
                    cryteria.delete()
            tag_to_delete.delete()

    filter = filters.TagFilter(request.GET,queryset=queryset)
    table = tables.TagsTable(filter.qs, order_by="-id") 
    RequestConfig(request,paginate={"per_page": 10,"paginator_class":LazyPaginator}).configure(table)
    return render(request, "tags.html",  {
        "form" : filter.form,
        "table": table
    })

def all_notes_view(request):
    queryset = models.LogsNote.objects.all()

    if request.method == "POST"and request.POST.__contains__("selected_notes"):
            notes_to_delete = request.POST.getlist("selected_notes")
            queryset.objects.filter(id__in=notes_to_delete).delete()

    filter = filters.NoteFilter(request.GET,queryset=queryset)
    table = tables.NotesTable(filter.qs, order_by="-id") 
    RequestConfig(request,paginate={"per_page": 10,"paginator_class":LazyPaginator}).configure(table)
    return render(request, "all_notes.html",  {
        "form" : filter.form,
        "table": table
    })

def all_notes_form_view(request,id=None,visitor_ip=None,transaction=None):
    if not id:
        note = models.LogsNote(visitor_ip=visitor_ip, transaction=transaction)
    else:
        note = get_object_or_404(models.LogsNote,pk=id)
        
    if request.method == "POST":
        form = forms.NoteForm(request.POST,instance=note)
        if form.has_changed() and form.is_valid():
            logsnote = form.save()
            if transaction:
                t = [models.Transaction.objects.get(pk=transaction)]
            else:   
                t = models.Transaction.objects.filter(Q(name__header_name=settings.VISITOR_IP) & Q(value__header_value=visitor_ip))
            logsnote.transactions.add(*t)
            return HttpResponseRedirect(reverse("all_notes"))
        return render(request, "all_notes_form.html", {"form" : form})
    
    form = forms.NoteForm(instance=note)
    return render(request, "all_notes_form.html", {"form" : form})