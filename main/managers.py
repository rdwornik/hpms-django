import re
from django.db.models import Q, Manager

from main import models


class LogsLogManager(Manager):
    def get_header_value(self,transaction, name):
        # TODO : error message
        try:
            return self.get(
                Q(transaction = transaction) &
                Q(name__header_name = name)
                ).value.header_value
        except models.LogsLog.MultipleObjectsReturned as e:
            pass

class LogsTagAssignManager(Manager):
    def assign_tags(self, logs_log_list):
        [
            [
                self.create(
                transaction = log.transaction,
                tag = tag)
                for tag in list(models.LogsTag.objects.filter(
                Q(name_cryteria = log.name
                )))
                if re.match(tag.value_cryteria,log.value.header_value)
            ]
            for log in logs_log_list
        ]