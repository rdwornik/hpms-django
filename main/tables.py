import django_tables2 as tables

from django.conf import settings
from django.utils.html import format_html
from django_tables2.utils import A  # alias for Accessor
from django.db.models import Q

from main import models
from main import utils
class VisitorTable(tables.Table):
    visitor_ip = tables.TemplateColumn(
        '<a href="{% url "transactions" %}?ip={{ record.id }}"> \
        {{ record.header_value}} \
        </a>',
        verbose_name="Visitors IP")
    visits = tables.Column(empty_values=(), verbose_name="Visits")
    add_note = tables.TemplateColumn(template_name="tables/add_note_column.html")
    class Meta:
        attrs = {
            "class": "table table-striped"
        }
class TransactionsDetailTable(tables.Table):
    class Meta:
        model = models.LogsLog
        exclude = ["transaction","id"]
        attrs = {
            "class": "table table-striped"
        }       
class TransactionsTable(tables.Table):
    id = tables.Column(
        orderable=False,
        visible=False
        )
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
        linkify=lambda value: value,
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
        attrs = {
            "class": "table  table-hover table-striped"
        }
        row_attrs = {
            "style": "transform: rotate(0);"
        }
    def render_request_uri(self, record):
        uri = record.logslog_set.filter(Q(name__header_name=settings.REQUEST_URI)).first()
        return uri.value.header_value  if uri else "None"
    def render_visitor_ip(self,record):
        visitor = record.logslog_set.filter(Q(name__header_name=settings.VISITORS_IP)).first()
        return visitor.value.header_value  if visitor else "None"
    def render_server(self, record):
        server = record.logslog_set.filter(Q(name__header_name=settings.SERVER_NAME)).first()
        return server.value.header_value  if server else "None"
    def render_transaction(self, value,record):
        request_method = record.logslog_set.filter(Q(name__header_name=settings.REQUEST_METHOD)).first()
        tag = request_method.value.header_value if request_method else "None"           
        letter, color = utils.get_or_create_methods_tag(tag)
        return format_html("{}<b><font color={}> {}</font></b>".format(value, color, letter))
    def render_tags(self, record):
        return format_html("".join("<b>{}</b> : {} <br/>"
                             .format(num, t.tag.tag) for num, t in enumerate(record.logstagassign_set.all(), start=1)))
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
        attrs = {
            "class": "table table-striped",
        }
