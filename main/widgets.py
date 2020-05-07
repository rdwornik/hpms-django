from django.forms.widgets import DateTimeInput
from dateutil.relativedelta import relativedelta
from django.forms.widgets import DateTimeInput, SplitDateTimeWidget
import datetime
class DateTimePickerInput(DateTimeInput):
    template_name = 'widgets/datetimepickerinput.html' 
    class Media:   
        css = {
            'all': ('css/datetimepickerinput.css',)
        }
        js = ('js/datetimepickerinput.js',)


