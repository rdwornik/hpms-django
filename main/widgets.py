from django.forms.widgets import DateTimeInput
from dateutil.relativedelta import relativedelta
import datetime
class DateTimePickerInput(DateTimeInput):
    template_name = 'widgets/datetimepickerinput.html'
    
    # def __init__(self, *args, **kwargs):
    #     print(kwargs['attrs'])
    #     super(DateTimePickerInput, self).__init__(*args, **kwargs)
        
    # def get_context(self, name, value, attrs):
    #     print(attrs)
    #     context = super().get_context(name, value, attrs)
    #     print(attrs)

    #     if int(name[-1]) == 0:
    #         context['widget']['value'] = (datetime.datetime.now() + relativedelta(years=-1)).strftime("%Y-%m-%d %H:%M")   
    #     else:
    #         context['widget']['value'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")   
    #     return context

        
