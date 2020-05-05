from django.forms.widgets import DateTimeInput
from dateutil.relativedelta import relativedelta
from django.forms.widgets import DateTimeInput, SplitDateTimeWidget
import datetime
class DateTimePickerInput(SplitDateTimeWidget):
    template_name = 'widgets/datetimepickerinput.html' 
    class Media:   
        css = {
            'all': ('css/datetimepickerinput.css',)
        }
        js = ('js/datetimepickerinput.js',)
    
    def decompress(self, value):
        print("hello")
        print(value)
        if value:
            return [value.date(), value.time()]
        return [None, None]