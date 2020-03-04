import django_tables2 as tables
from main import models
from main import utils
from django.utils.html import format_html

REQUEST_METHOD = 'REQUEST_METHOD'



class VisitorTable(tables.Table):
    visitor_ip = tables.Column(empty_values=(), verbose_name="Visitors IP")
    visits = tables.Column(empty_values=(), verbose_name="Visits")
    # class Meta:
    #     attrs = {"class": "floatLeft"}

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
        
    # def render_request_uri(self, value, record):
    #     pass
        # uri = self.objects.get()
        # print(self.data.data.all())
        # return "<%s>" % record
    # def render_row_number(self):
    #     return "Row %d" % next(self.counter)
    # def render_request_uri(self):
    #     return "Row %d" % next(self.counter)
    # def render_id(self, value, record):
    #     # print(type(record))
    #     # print(record.transaction)
    #     # print(self)
    #     return "<%s>" % record

