import re
from django.db.models import Q, Manager

from main import models

class LogsTagAssignManager(Manager):
    def assign_tags_on_logs_created(self, logs_log_list):
        [
            [
                self.create(transaction = log.transaction,tag = tag)
                for tag in models.LogsTag.objects.filter(Q(name_cryteria = log.name))
                if re.match(tag.value_cryteria,log.value.header_value)
            ]
            for log in logs_log_list
        ]
    def assign_tags_on_tags_created_or_updated(self, tag, edited):
        if edited:
            self.filter(Q(tag=tag)).delete()
            
        logs_to_tag = models.LogsLog.objects.filter(
            Q(name__header_name = tag.name_cryteria) &
            Q(value__header_value__iregex=tag.value_cryteria))

        if logs_to_tag.exists():
            [ self.create(tag=tag, transaction=log.transaction) for log in logs_to_tag ]
