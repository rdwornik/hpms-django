
from django.db import models
from main import managers

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re

def validate_regex(value):
    try:
        re.compile(value)
    except re.error:
        raise ValidationError(
        _(' %(value)s is not an valid regular expression'),
        params={'value': value},
        )
        
# Create your models here.
class HeaderName(models.Model):
    header_name = models.TextField(unique=True)

    def __str__(self):
        return "{0}".format(self.header_name)
    class Meta:
        ordering = ('header_name',)

    
class HeaderValue(models.Model):
    header_value = models.TextField(unique=True)
    header_names = models.ManyToManyField(HeaderName, through="LogsLog")

    class Meta:
        ordering = ('header_value',)

    def __str__(self):
        return "{0}".format(self.header_value)
    
class TagCryteria(models.Model):
    name_cryteria = models.ForeignKey(HeaderName,on_delete=models.CASCADE)
    value_cryteria = models.TextField(validators=[validate_regex])
    
    class Meta:
        verbose_name = "Tag Cryteria"
        verbose_name_plural = "Tag Cryterias"
    def __str__(self):
        return "{0} {1}".format(self.name_cryteria,self.value_cryteria)
    
class LogsTag(models.Model):
    cryterias = models.ManyToManyField(TagCryteria)
    tag_name = models.TextField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Logs Tag"
        verbose_name_plural = "Logs Tags"
        ordering = ('-id',)

    def __str__(self):
        return "{0} {1}".format(self.id,self.tag_name)
    
class Transaction(models.Model):
    transaction = models.BigAutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    assigned_tags = models.ManyToManyField(LogsTag, through="LogsTagAssign")
    name = models.ManyToManyField(HeaderName,through="LogsLog")
    value = models.ManyToManyField(HeaderValue,through="LogsLog")

    class Meta:
        verbose_name ="Transaction"
        verbose_name_plural = "Transactions"
        ordering = ('-transaction',)
        
    def __str__(self):
        return "{}".format(self.time)
    
class LogsLog(models.Model):
    name = models.ForeignKey(HeaderName,on_delete=models.CASCADE)
    value = models.ForeignKey(HeaderValue,on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "LogsLog"
        verbose_name_plural = "LogsLogs"
        
    def __str__(self):    
         return "{0} {1} {2}".format(self.name, self.value,self.transaction)

class LogsNote(models.Model):
    id = models.AutoField(primary_key = True)
    transactions = models.ManyToManyField(Transaction)
    title = models.TextField()
    content = models.TextField()
    transaction = models.IntegerField(blank=True,null=True,default=1)
    visitor_ip = models.GenericIPAddressField()    
    class Meta:
        verbose_name = "LogsNote"
        verbose_name_plural = "LogsNotes"
        ordering = ('-id',)

        
    def __str__(self):
         return "title {0} content {1} ip {2} trans {3}".format(self.title, self.content, self.visitor_ip, self.transaction)
        
class LogsTagAssign(models.Model):
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE)
    tag = models.ForeignKey(LogsTag,on_delete=models.CASCADE)
    
    objects = managers.LogsTagAssignManager()

    class Meta:
        verbose_name = "Log Tag Assignment"
        verbose_name_plural = "Log Tag Assignments"

    def __str__(self):
        return "{0} {1}".format(self.transaction, self.tag)