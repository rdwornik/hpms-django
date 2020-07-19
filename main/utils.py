import random 
from dateutil.relativedelta import relativedelta
from django.db.models import functions as functions

'''
Moment.js string format
Name	     Default	      Example
millisecond	'h:mm:ss.SSS a'	 '11:20:01.123 AM'
second	    'h:mm:ss a'	     '11:20:01 AM'
minute	    'h:mm a'	     '11:20 AM'
hour	    'hA'	         '11AM'
day	        'MMM D'	         'Sep 4'
week	    'll'	        'Sep 4 2015'
month	    'MMM YYYY'	     'Sep 2015'
quarter	    '[Q]Q - YYYY'	 'Q3 - 2015'
year	    'YYYY'	         '2015'
'''

methods = {
    "GET"  : ("G","008000"),
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
    "minute" : lambda td : td.days == 0 and 0 < (td.seconds)  < 3600,
    "hour": lambda td :  td.days == 0 and 0 < (td.seconds)//3600 < 24 ,
    "day": lambda td :  0 < td.days <= 31 ,
    # "week" : lambda td : 7 < td.days <= 62,
    "month" : lambda td : 31 < td.days <= 450 ,
    "year" : lambda td :  450 < td.days,
}

display_format = {
    "second" : "HH:mm:ss",
    "minute" : "HH:mm",
    "hour": "HH",
    "day":   "DD.MM",
    # "week" : "DD.MM.YY",
    "month" : "MMM YYYY",
    "year" : "YYYY",
}

trunc_methods_chart = {
    "second" :  functions.TruncSecond,
    "minute" :  functions.TruncMinute,
    "hour":     functions.TruncHour,
    "day":      functions.TruncDay,
    "month":    functions.TruncDay,
    "year":     functions.TruncDay,
}

trunc_methods_table = {
    "minute" :  functions.TruncMinute,
    "hour":     functions.TruncHour,
    "day":      functions.TruncDay,
    "month":    functions.TruncMonth,
    "year":     functions.TruncYear,
}

get_current_date = {
    "minute"    :  lambda date : date.strftime("%H:00"), 
    "hour"      :  lambda date : date.strftime("%d %b %Y"),  
    "day"       :  lambda date : date.strftime("%b %Y"),  
    "month"     :  lambda date : date.strftime("%Y"), 
    "year"      :  lambda date : "Years",  
}

format_table_date = {
    "minute"    :  lambda date : date.strftime("%M:00 - %M:59"),  
    "hour"      :  lambda date : date.strftime("%H:00 - %H:59"),
    "day"       :  lambda date : date.strftime("%d.%m"),      
    "month"     :  lambda date : date.strftime("%B"), 
    "year"      :  lambda date : date.strftime("%Y"),  
}

#tuple is returned
get_previous_and_next = {
    "minute": lambda time_after, time_before: ( {"time_after": (time_after + relativedelta(hours=-1 )).strftime('%Y-%m-%d %H:%M'),  "time_before": (time_before + relativedelta(hours=-1)).strftime('%Y-%m-%d %H:%M')},  {"time_after": (time_after + relativedelta(hours=+1)).strftime('%Y-%m-%d %H:%M') ,"time_before": (time_before + relativedelta(hours=+1    )).strftime('%Y-%m-%d %H:%M')   }),
    "hour"  : lambda time_after, time_before: ( {"time_after": (time_after + relativedelta(days=-1  )).strftime('%Y-%m-%d %H:%M'),  "time_before": (time_before + relativedelta(days=-1)).strftime('%Y-%m-%d %H:%M')},  {"time_after": (time_after + relativedelta(days=+1)).strftime('%Y-%m-%d %H:%M') ,"time_before": (time_before + relativedelta(days=+1       )).strftime('%Y-%m-%d %H:%M')   }),
    "day"   : lambda time_after, time_before: ( {"time_after": (time_after + relativedelta(months=-1)).strftime('%Y-%m-%d %H:%M'),  "time_before": (time_before + relativedelta(months=-1)).strftime('%Y-%m-%d %H:%M')},  {"time_after": (time_after + relativedelta(months=+1)).strftime('%Y-%m-%d %H:%M') ,"time_before": (time_before + relativedelta(months=+1 )).strftime('%Y-%m-%d %H:%M')   }),
    "month" : lambda time_after, time_before: ( {"time_after": (time_after + relativedelta(years=-1 )).strftime('%Y-%m-%d %H:%M'),  "time_before": (time_before + relativedelta(years=-1)).strftime('%Y-%m-%d %H:%M')},  {"time_after": (time_after + relativedelta(years=+1)).strftime('%Y-%m-%d %H:%M') ,"time_before": (time_before + relativedelta(years=+1    )).strftime('%Y-%m-%d %H:%M')   }),
    "year"  : lambda time_after, time_before: ( {"time_after": (time_after + relativedelta(years=-10)).strftime('%Y-%m-%d %H:%M'),  "time_before": (time_before + relativedelta(years=-10)).strftime('%Y-%m-%d %H:%M')},  {"time_after": (time_after + relativedelta(years=+10)).strftime('%Y-%m-%d %H:%M') ,"time_before": (time_before + relativedelta(years=+10 )).strftime('%Y-%m-%d %H:%M')   }),                      
}

get_time_after_and_before = {
    "minute"    : lambda date: (date.strftime('%Y-%m-%d %H:%M'), (date + relativedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')),       
    "hour"      : lambda date: (date.strftime('%Y-%m-%d %H:%M'), (date + relativedelta(hours=1)     + relativedelta(minutes=-1) ).strftime('%Y-%m-%d %H:%M')),   
    "day"       : lambda date: (date.strftime('%Y-%m-%d %H:%M'), (date + relativedelta(days=1)      + relativedelta(hours=-1)   ).strftime('%Y-%m-%d %H:%M')),
    "month"     : lambda date: (date.strftime('%Y-%m-%d %H:%M'), (date + relativedelta(months=1)    + relativedelta(days=-1)    ).strftime('%Y-%m-%d %H:%M')),
}