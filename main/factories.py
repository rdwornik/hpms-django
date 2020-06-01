import factory

from datetime import datetime
from main import models

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Transaction
    time = datetime.now()
    transaction = factory.Sequence(int)

class LogsLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogsLog
        
class TagCryteriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TagCryteria

class LogsNoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogsNote
class HeaderNameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HeaderName
        
class HeaderValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HeaderValue

class LogsTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogsTag
    tag_name = "test"
    description = "test"
class LogsTagAssignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LogsTagAssign
    