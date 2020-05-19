from django.forms.widgets import DateTimeInput
class DateTimePickerInput(DateTimeInput):
    template_name = 'widgets/datetimepickerinput.html' 
    class Media:   
        css = {
            'all': ('css/datetimepickerinput.css',)
        }
        js = ('js/datetimepickerinput.js',)


