import django_tables2 as tables
from main import models
from main import utils
from django.utils.html import format_html

REQUEST_METHOD = 'REQUEST_METHOD'
REQUEST_URI = 'REQUEST_URI'
VISITORS_IP = 'VISITORS_IP'

class TagsCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})
        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
        return format_html("<p><label><input %s/><span></span></label></p>" % attrs.as_html())

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
    tag = tables.Column(
        linkify=lambda record: "{}/edit/".format(record.id),
        attrs={
            "td":{
                "scope" : "row" ,
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
    # checkbox = tables.TemplateColumn(
    #     "<input class='action-select' type='checkbox' name='_selected_tags' value='{{ record.id }}' />",
    #     verbose_name="",
    #     attrs={
    #         "td":{
    #             "style":"word-break: break-all"
    #         },
    #         "th":{
    #             "style":"width: 1%"
    #         }
    #     })
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={
            "th":{
                "style":"width: 2%",
            },
            "th__input":{
                "id":"action-toggle",
                "onclick":"toggle(this)"
            },
            "td__input":{
                "name" : "selected_tags",
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
    # id = tables.Column(
    #     attrs={
    #         "td":{
    #             "style":"word-break: break-all"
    #         },
    #         "th":{
    #             "style":"width:1%"
    #         }
    #     })
    # def is_checked(value, record):
    #     print(value)
    #     print(record)
    #     return True
    class Meta:
        models = models.LogsTag
        sequence = ('selection', 'tag', 'name_cryteria', 'value_cryteria', 'description')
        attrs = {
            "class": "table table-striped",
            "id" : "tags-list"
        }
