import django_tables2 as tables
from main import models
from main import utils
from django.utils.html import format_html
from django_tables2.utils import A  # alias for Accessor

REQUEST_METHOD = 'REQUEST_METHOD'



class VisitorTable(tables.Table):
    visitor_ip = tables.TemplateColumn('<a href="../transactions/?ip={{ record.value_id }}">{{ record.value__header_value }}</a>')
    visits = tables.Column(empty_values=(), verbose_name="Visits")

    # def render_visitor_ip(self,record):
    #     print(record)
    #     print(self.data.data.all())
    #     return "{}".format(record['value__header_value'])


class NetworkTable(tables.Table):
    network = tables.Column(empty_values=(), verbose_name="Network")
    visits = tables.Column(empty_values=(), verbose_name="Visits")
    hosts = tables.Column(empty_values=(), verbose_name="Hosts")

    # class Meta:
    #     attrs = {"class": "floatRight"}

class TransactionsTable(tables.Table):
    # request_uri = tables.Column(verbose_name='REQUEST URI',empty_values=())
    # row_number = tables.Column(empty_values=())
    # id = tables.Column()
    # transaction = tables.Column(attrs={"td": {"style": "font-weight:bold; color:red;"}})
    transaction = tables.Column()
    time = tables.DateTimeColumn(format="d F Y H:i:s")
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.objects = self.data.model.objects
        
    class Meta:
        model = models.LogsLog
        exclude = ('name',)
        attrs = {
            "class": "table table-striped"
        }

    def render_transaction(self, value, record):
        header_value = self.objects.get_header_value(value,REQUEST_METHOD)
        tag = utils.methods[header_value]
        return format_html("{} <b><font color={}>{}</font></b>", value, tag[1], tag[0])

