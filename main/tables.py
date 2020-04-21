import django_tables2 as tables
import json
from main import models
from main import utils
from django.conf import settings
from django.utils.html import format_html
from django_tables2.utils import A  # alias for Accessor
from django.db.models import Q

class VisitorTable(tables.Table):
    visitor_ip = tables.TemplateColumn(
        '<a href="{% url "transactions" %}?ip={{ record.value_id }}"> \
        {{ record.value__header_value }} \
        </a>',
        verbose_name="Visitors IP")
    visits = tables.Column(empty_values=(), verbose_name="Visits")
    class Meta:
        attrs = {
            "class": "table table-striped"
        }

class TransactionsDetailTable(tables.Table):
    class Meta:
        model = models.LogsLog
        exclude = ["transaction","id","time"]
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
        model = models.LogsLog
        exclude = ("name","value")
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
        return self.data.model.objects.get_header_value(record.transaction,settings.REQUEST_URI)
    def render_visitor_ip(self,record):
        return self.data.model.objects.get_header_value(record.transaction,settings.VISITORS_IP)
    def render_server(self, record):
        return self.data.model.objects.get_header_value(record.transaction,settings.SERVER_NAME)

    def render_transaction(self, value):
        request_method = self.data.model.objects.get_header_value(value,settings.REQUEST_METHOD)
        tag = utils.get_or_create_methods_tag(request_method)
        color, letter = tag[1], tag[0]
        return format_html("{}<b><font color={}> {}</font></b>".format(value, color, letter))
    def render_tags(self, record):
        assigned_tags = models.LogsTagAssign.objects.filter(Q(transaction=record.transaction)).values("tag_id")
        tags = {}
        for num, t in enumerate(assigned_tags, start=1):
            tags[num] = models.LogsTag.objects.get(pk=t["tag_id"]).tag
        return format_html("".join("<b>{}</b> : {} <br/>".format(k, v) for k, v in tags.items()))
    def order_time(self, queryset, is_descending):
        queryset = queryset.order_by(
                                    ("-" if is_descending else "") + 
                                     "transaction",("-" if is_descending else "") + 
                                     "time").distinct("transaction")
        return (queryset,True)
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
