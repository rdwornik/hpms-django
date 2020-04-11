import django.dispatch

tag_submited = django.dispatch.Signal(providing_args=["tag","edited"])
