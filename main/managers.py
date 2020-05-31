import re
from django.db.models import Q, Manager
from main import models

class LogsTagAssignManager(Manager):
    def assign_tags_on_transaction_created(self, logs_log_list):
        cryterias = []
        for log in logs_log_list:
            for cryteria in models.TagCryteria.objects.filter(Q(name_cryteria = log.name)):
                if re.match(cryteria.value_cryteria,log.value.header_value):
                    cryterias.append(cryteria)
        tags = models.LogsTag.objects.filter(cryterias__in=cryterias)
        for tag in tags:
            if set(tag.cryterias.all()) & set(cryterias) == set(tag.cryterias.all()):
                self.create(transaction = log.transaction,tag = tag)
        
    def assign_tags_on_tags_created(self, tag, edited):
        if edited:
            self.filter(tag=tag).delete()
        
        transactions= models.Transaction.objects.all()
 
        for cryteria in tag.cryterias.all():
            transactions = transactions.filter(
                Q(name__header_name = cryteria.name_cryteria) &
                Q(value__header_value__iregex=cryteria.value_cryteria))
  
        if  transactions.exists():
            [ self.create(tag=tag, transaction=transaction) for transaction in transactions]