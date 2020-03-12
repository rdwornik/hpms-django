import django.dispatch

methods = {
    'GET' : ('G','green'),
    'POST' : ('P','blue'),
    'HEAD' : ('H', 'yellow')
}

transaction_done = django.dispatch.Signal(providing_args=["transaction"])
