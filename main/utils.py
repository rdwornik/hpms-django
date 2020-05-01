from dateutil.relativedelta import relativedelta
import datetime
from main.serializers import DateTimeFieldSerializer, DateFieldSerializer
import random 
from django.db.models.functions import TruncDay, TruncHour, TruncYear, TruncMonth, TruncMinute, TruncSecond
from django.db.models import Count, DateTimeField, TimeField, DateField

methods = {
    "GET" : ("G","008000"),
    "POST" : ("P","0000FF"),
    "HEAD" : ("H", "FFFF00")
}
def get_or_create_methods_tag(request_method):
    if request_method not in methods:
        i = 0
        tag = request_method[i]
        color = "%06x" % random.randint(0, 0xFFFFFF)
        tags = [tag[0] for tag in methods.values()]
        colors = [color[1] for color in methods.values()]
        while request_method[i] in tags:
            i += 1
            tag += request_method[i]
        while color in colors:
            color = "%06x" % random.randint(0, 0xFFFFFF)
        methods[request_method] = (tag, color)
    return methods[request_method]


range = {
    "second" : lambda td: 0 < td.seconds < 60,
    "minute" : lambda td : td.days == 0 and 0 < (td.seconds)//60 % 60 != 0,
    "hour": lambda td :  td.days == 0 and 0 < (td.seconds)//3600 < 24 ,
    "day": lambda td :  0 < td.days <= 62 ,
    # "week" : lambda td : 7 < td.days <= 62,
    "month" : lambda td : 62 < td.days <= 450 ,
    "year" : lambda td :  450 < td.days,
}

display_format = {
    "second" : "ss",
    "minute" : "mm",
    "hour": "HH",
    "day":   "DD.MM",
    "week" : "wo",
    "month" : "MMM",
    "year" : "YYYY",
}

generate_label = {
   "minute" : lambda date1, date2 : [(date1 + relativedelta(minutes=+x)).isoformat() for x in range(0,(date2 - date1).seconds//60 % 60 +1)],
   "hour": lambda date1, date2 : [(date1 + relativedelta(hours=+x)).strftime("%H") for x in range(0,relativedelta(date1,date2).hours+1)],
   "week" : lambda date1, date2 : [(date1 + relativedelta(weeks=+x)).strftime("%a") for x in range(0,relativedelta(date1,date2).weeks+1)], 
   "month": lambda date1, date2 : [(date1 + relativedelta(months=+x)).strftime("%b") for x in range(0,relativedelta(date1,date2).months+1)],
   "year": lambda date1, date2 : [(date1 + relativedelta(years=+x)).strftime("%Y") for x in range(0,relativedelta(date1,date2).years+1)],
}


select_trunc_method = {
    "hour": lambda td :  td.days == 0 and 0 < (td.seconds)//3600 < 24,
    "day": lambda td :  0 < td.days,
}

trunc_methods = {
    "second" : (TruncSecond, DateTimeField, DateTimeFieldSerializer),
    "minute" : (TruncMinute, DateTimeField, DateTimeFieldSerializer),
    "hour": (TruncHour, DateTimeField, DateTimeFieldSerializer),
    "day": (TruncDay, DateField, DateFieldSerializer),
    "month": (TruncDay, DateField, DateFieldSerializer),
    "year": (TruncDay, DateField, DateFieldSerializer),
}

date_order = lambda date1, date2: (date1, date2) if date1 < date2 else (date2,date1) 
time_delta = lambda date1, date2 : date2 - date1

