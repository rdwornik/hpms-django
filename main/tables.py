import django_tables2 as tables
from main import models
from main import utils
from django.utils.html import format_html
from django_tables2.utils import A  # alias for Accessor

REQUEST_METHOD = 'REQUEST_METHOD'
REQUEST_URI = 'REQUEST_URI'
VISITORS_IP = 'VISITORS_IP'



class VisitorTable(tables.Table):
    visitor_ip = tables.TemplateColumn('<a href="..{% url "transactions" %}?ip={{ record.value_id }}">{{ record.value__header_value }}</a>',verbose_name="Visitors IP")
    visits = tables.Column(empty_values=(), verbose_name="Visits")

class TransactionTable(tables.Table):
    class Meta:
        model = models.LogsLog
        exclude = ['server','transaction','id','time']
        attrs = {
            "class": "table table-striped"
        }
class TransactionsTable(tables.Table):
    transaction = tables.Column(
        linkify=lambda value: value,
        attrs={"td" : { "scope" : "row" },
                "a" : { "class" :  "stretched-link" }
                })
    time = tables.DateTimeColumn(format="d F Y H:i:s")
    visitor_ip = tables.Column(verbose_name="Visitor IP",empty_values=(),orderable=False)
    request_uri = tables.Column(verbose_name='Request URI',empty_values=(),orderable=False)
    id = tables.Column(orderable=False)
    server = tables.Column(orderable=False)

    class Meta:
        model = models.LogsLog
        exclude = ('name','value')
        sequence =('id','transaction','time','visitor_ip','request_uri','server')
        attrs = {
            "class": "table  table-hover table-striped"
        }
        row_attrs = {
            "style": "transform: rotate(0);"
        }
    def render_request_uri(self, record):
        return self.data.model.objects.get_header_value(record.transaction,REQUEST_URI)
    def render_visitor_ip(self,record):
        return self.data.model.objects.get_header_value(record.transaction,VISITORS_IP)
    def render_transaction(self, value):
        header_value = self.data.model.objects.get_header_value(value,REQUEST_METHOD)
        tag = utils.methods[header_value]
        return format_html("{}<b><font color={}> {}</font></b>".format(value, tag[1], tag[0]))
    def order_time(self, queryset, is_descending):
        queryset = queryset.order_by(("-" if is_descending else "") + "transaction",("-" if is_descending else "") + "time").distinct('transaction')
        return (queryset,True)
class TagsTable(tables.Table):
    id = tables.Column(visible=False)
    tag = tables.LinkColumn(
        "action_tag_edit",
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
        sequence = ('id','selection', 'tag', 'name_cryteria', 'value_cryteria', 'description')
        attrs = {
            "class": "table table-striped",
            "id" : "tags-list"
        }
