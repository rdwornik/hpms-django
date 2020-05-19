from dateutil.relativedelta import relativedelta
import datetime
import random 
from django.db.models.functions import TruncDay, TruncHour, TruncYear, TruncMonth, TruncMinute, TruncSecond
from django.db.models import Count, DateTimeField, TimeField, DateField

methods = {
    "GET" : ("G","008000"),
    "POST" : ("P","0000FF"),
    "HEAD" : ("H", "FFFF00"),
    "None" : ("None","000000")
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


time_range = {
    "second" : lambda td: 0 < td.seconds < 60,
    "minute" : lambda td : td.days == 0 and 0 < (td.seconds)//60 % 60 != 0,
    "hour": lambda td :  td.days == 0 and 0 < (td.seconds)//3600 < 24 ,
    "day": lambda td :  0 < td.days <= 62 ,
    # "week" : lambda td : 7 < td.days <= 62,
    "month" : lambda td : 62 < td.days <= 450 ,
    "year" : lambda td :  450 < td.days,
}
'''
Moment.js string format
Name	     Default	      Example
millisecond	'h:mm:ss.SSS a'	 '11:20:01.123 AM'
second	    'h:mm:ss a'	     '11:20:01 AM'
minute	    'h:mm a'	     '11:20 AM'
hour	    'hA'	         '11AM'
day	        'MMM D'	         'Sep 4'
week	    'll'	         'Sep 4 2015'
month	    'MMM YYYY'	     'Sep 2015'
quarter	    '[Q]Q - YYYY'	 'Q3 - 2015'
year	    'YYYY'	         '2015'
'''

display_format = {
    "second" : "HH:mm:ss",
    "minute" : "HH:mm",
    "hour": "HH",
    "day":   "DD.MM",
    # "week" : "DD.MM.YY",
    "month" : "MMM YY",
    "year" : "YYYY",
}

select_trunc_method = {
    "hour": lambda td :  td.days == 0 and 0 < (td.seconds)//3600 < 24,
    "day": lambda td :  0 < td.days,
}

trunc_methods = {
    "second" : TruncSecond,
    "minute" : TruncMinute,
    "hour": TruncHour,
    "day": TruncDay,
    "month": TruncDay,
    "year": TruncDay,
}

date_order = lambda date1, date2: (date1, date2) if date1 < date2 else (date2,date1) 
time_delta = lambda date1, date2 : date2 - date1

