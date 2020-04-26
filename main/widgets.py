from django.forms.widgets import DateTimeInput

class DateTimePickerInput(DateTimeInput):
    template_name = 'widgets/datetimepickerinput.html'