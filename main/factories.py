import factory
import factory.fuzzy

from datetime import datetime
from main import models

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Transaction
    time = datetime.now()

class LogsLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogsLog

class HeaderNameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HeaderName

class HeaderValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HeaderValue

class LogsTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogsTag
    tag = "test"
    description = "test"
    
class LogsTagAssignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogsTagAssign
    