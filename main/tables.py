import django_tables2 as tables
from django.conf import settings
from django.utils.html import format_html
from django_tables2.utils import A  # alias for Accessor
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from main import models
from main import utils
#TODO wywalic range z activity
#TODO wycentrowac tabele

class ActivityTable(tables.Table):
    date = tables.Column(attrs={
            "td": {"align": "center"}
        })
    visits_count = tables.Column(verbose_name="Count",attrs={
            "td": {"align": "center"}
        })
    
    def render_date(self,value, record):
        time_range = self.context.get('time_range')
        displayed_value = utils.format_table_date[time_range](value)
        updated = self.request.GET.copy()
        updated["time_after"], updated["time_before"] = (utils.get_time_after_and_before[time_range])(value)
        return displayed_value if time_range == "minute" else format_html("<a href='{0}?{1}' >{2}</a>".format(reverse_lazy("activity"), updated.urlencode(),displayed_value))
    def render_visits_count(self, value, record):
        time_range = self.context.get('time_range')
        updated = self.request.GET.copy()
        updated["time_after"], updated["time_before"] = (utils.get_time_after_and_before[time_range])(record['date'])
        return format_html("<a href='{0}?{1}' >{2}</a>".format(reverse_lazy("transactions"), updated.urlencode(),value))
    
    class Meta:
        attrs = {"style" : "width:100%;"}
class NotesTable(tables.Table):
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={
            "th":{
                "style":"width: 2%"
            },
            "td__input":{
                "name" : "selected_notes",
            },
            "th__input":{
                "type" : "hidden"
            }
        })
    title = tables.LinkColumn("all_notes_edit", text=lambda record: record.title, args=[A("pk")])

    class Meta:
        model = models.LogsNote
        exclude = ["id"]
        sequence = ("selection","title","content","visitor_ip","transaction")  
class VisitorTable(tables.Table):
    visitor_ip = tables.TemplateColumn(template_name="tables/visitor_ip_column.html",orderable=False,verbose_name="Visitors IP")
    visits = tables.Column(empty_values=(), verbose_name="Visits")
    add_note = tables.TemplateColumn(template_name="tables/add_note_column.html",orderable=False,verbose_name="")  
class TransactionsDetailTable(tables.Table):
    class Meta:
        model = models.LogsLog
        exclude = ["transaction","id"]
        attrs = {
            "class": "table table-striped"
        }       
class TransactionsTable(tables.Table):
    id = tables.Column(orderable=False, visible=False)
    visitor_ip = tables.Column(
        verbose_name="Visitor IP",
        empty_values=(),
        orderable=False,
        attrs={
            "td":{
                "style":"word-break: break-all",
            },
            "th":{
                "style":"width: 10%"
            }
        })
    request_uri = tables.Column(
        verbose_name="Request URI",
        empty_values=(),
        orderable=False,
        attrs={
            "td":{
                "style":"word-break: break-all",
            },
            "th":{
                "style":"width: 25%"
            }
        })
    server = tables.Column(
        empty_values=(),
        orderable=False,
        attrs={
            "td":{
                "style":"word-break: break-all",
            },
            "th":{
                "style":"width: 15%"
            }
        })
    transaction = tables.Column(
        linkify=lambda record: reverse("transactions_detail", 
                                       kwargs={"visitor_ip": record.logslog_set.filter(Q(name__header_name=settings.VISITOR_IP)).first().value.pk,
                                               "transaction": record.transaction}),        
        attrs={
                "td" : { 
                    "scope" : "row",
                    "style": "word-break: break-all"
                    },
                "th":{
                    "style":"width: 10%"
                },                
                "a" : { "class" :  "stretched-link" }
        })
    time = tables.DateTimeColumn(
        format="d F Y H:i:s",
        orderable=False,
        attrs={
            "td":{
                "style":"word-break: break-all",
            },
            "th":{
                "style":"width: 15%"
            }
        })
    tags = tables.Column(
        empty_values=(),
        orderable=False,
        attrs={
            "td":{
                "style":"word-break: break-all",
            },
            "th":{
                "style":"width: 25%"
            }
        })
    class Meta:
        model = models.Transaction
        exclude = ("assigned_tags",)
        sequence =("id",
                   "transaction",
                   "time",
                   "visitor_ip",
                   "server",
                   "request_uri",
                   "tags")
        row_attrs = {
            "style": "transform: rotate(0);"
        }
    def render_request_uri(self, record):
        uri = record.logslog_set.filter(Q(name__header_name=settings.REQUEST_URI)).first()
        return uri.value.header_value  if uri else "None"
    def render_server(self, record):
        server = record.logslog_set.filter(Q(name__header_name=settings.SERVER_NAME)).first()
        return server.value.header_value  if server else "None"
    def render_tags(self, record):
        return format_html("".join("<b>{}</b> : {} "
                             .format(num, t.tag.tag) for num, t in enumerate(record.logstagassign_set.all(), start=1)))
    def render_visitor_ip(self,record):
        visitor = record.logslog_set.filter(Q(name__header_name=settings.VISITOR_IP)).first()
        visitor_id = visitor.value_id  if visitor else "None"
        visitor_header_value = visitor.value.header_value  if visitor else "None"
        notes_count = models.LogsNote.objects.filter(visitor_ip=visitor_header_value).count()
        return format_html("<a href='{0}?visitor_ip={1}' style='z-index: 2; position:relative'>{2} </a>\
                            <a href='{3}?visitor_ip={2}' style='z-index: 2; position:relative'>[{4}]</a>".format( reverse_lazy("transactions"),
                                                                                                                visitor_id,
                                                                                                                visitor_header_value,
                                                                                                                reverse_lazy("all_notes"),
                                                                                                                notes_count))
    def render_transaction(self, value,record):
        request_method = record.logslog_set.filter(Q(name__header_name=settings.REQUEST_METHOD)).first()
        notes_count = record.logsnote_set.filter(transaction=record.transaction).count()
        tag = request_method.value.header_value if request_method else "None"         
        letter, color = utils.get_or_create_methods_tag(tag)
        return format_html("{0}<b><font color={1}> {2}</font></b> \
                              <a href='{3}?transaction={0}' style='z-index: 2; position:relative'>[{4}]</a>".format(value, 
                                                                                                                    color, 
                                                                                                                    letter,
                                                                                                                    reverse_lazy('all_notes'),
                                                                                                                    notes_count))

class TagsTable(tables.Table):
    id = tables.Column(visible=False)
    tag = tables.LinkColumn(
        "tags_edit",
        text=lambda value: value, args=[A("pk")],
        attrs={
            "td":{
                "style":"word-break: break-all",
            },
            "th":{
                "style":"width: 13%"
            }
        })
    name_cryteria = tables.Column(
        attrs={
            "td":{
                "style":"word-break: break-all"
            },
            "th":{
                "style":"width: 28%"
            }
        })
    value_cryteria = tables.Column(
        attrs={
            "td":{
                "style":"word-break: break-all"
            },
            "th":{
                "style":"width: 20%"
            }
        })
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={
            "th":{
                "style":"width: 2%"
            },
            "td__input":{
                "name" : "selected_tags",
            },
            "th__input":{
                "type" : "hidden"
            }
        }
        )
    description = tables.Column(
        attrs={
            "td":{
                "style":"word-break: break-all"
            },
            "th":{
                "style":"width:38%"
            }
        })
    class Meta:
        models = models.LogsTag
        sequence = ("id","selection", "tag", "name_cryteria", "value_cryteria", "description")
