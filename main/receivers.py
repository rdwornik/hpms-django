import re

from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db.models import Q
from .signals import *
from main import models

@receiver(tag_submited)
def assign_tag_on_submit(sender, **kwargs):
    edited = kwargs.pop("edited")
    tag = kwargs.pop("tag")

    if edited:
        sender.objects.filter(Q(tag=tag)).delete()

    logs_to_tag = models.LogsLog.objects.filter(
        Q(name_id = tag.name_cryteria_id) &
        Q(value__header_value__iregex=tag.value_cryteria)
        ).values_list("transaction")
    
    if logs_to_tag:
        tags_assigned = [
            sender(
                tag=tag,
                transaction=transaction[0]
            ) for transaction in logs_to_tag
        ]
        sender.objects.bulk_create(tags_assigned)
