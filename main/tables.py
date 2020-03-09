import django_tables2 as tables
from main import models
from main import utils
from django.utils.html import format_html

REQUEST_METHOD = 'REQUEST_METHOD'
class VisitorTable(tables.Table):
    visitor_ip = tables.TemplateColumn('<a href="..{% url "transactions" %}?ip={{ record.value_id }}">{{ record.value__header_value }}</a>',verbose_name="Visitors IP")
    # visitor_ip = tables.Column(
    #     empty_values=(),
    #     linkify=lambda record : '..{% url "transactions" %}?ip={}'.format(record['value_id']),
    #     verbose_name="Visitors IP")
    visits = tables.Column(empty_values=(), verbose_name="Visits")
    # def render_visitor_ip(self,record):
    #     print(record)
    #     # print(self.data.data.all())
    #     return "{}".format(record['value__header_value'])
class TransactionTable(tables.Table):
    class Meta:
        model = models.LogsLog
        exclude = ['server','transaction','id','time']
        attrs = {
            "class": "table table-striped"
        }
class TransactionsTable(tables.Table):
    # request_uri = tables.Column(verbose_name='REQUEST URI',empty_values=())
    # row_number = tables.Column(empty_values=())
    # id = tables.Column()
    # transaction = tables.Column(attrs={"td": {"style": "font-weight:bold; color:red;"}})
    transaction = tables.Column(
        linkify=lambda value: value,
        attrs={"td" : { "scope" : "row" },
                "a" : { "class" :  "stretched-link" }
                })
    time = tables.DateTimeColumn(format="d F Y H:i:s")
    class Meta:
        model = models.LogsLog
        exclude = ('name',)
        attrs = {
            "class": "table  table-hover table-striped"
        }
        row_attrs = {
            "style": "transform: rotate(0);"
        }

    def render_transaction(self, value, record):
        header_value = self.data.model.objects.get_header_value(value,REQUEST_METHOD)
        tag = utils.methods[header_value]
        return format_html("{}<b><font color={}> {}</font></b>".format(value, tag[1], tag[0]))
    #     return format_html('<th scope="row"><a href="{}" class="stretched-link"><b><font color={}>{}</font></b></a></th>',value,tag[1],tag[0])
    #     # return value
