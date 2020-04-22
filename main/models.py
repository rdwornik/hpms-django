
from django.db import models
from  django.utils import timezone
from main import utils, managers
# Create your models here.
class HeaderName(models.Model):
    header_name = models.TextField(unique=True)
    def __str__(self):
        return "{0}".format(self.header_name)
    
class HeaderValue(models.Model):
    header_value = models.TextField(unique=True)
    header_names = models.ManyToManyField(HeaderName, through="LogsLog")

    def __str__(self):
        return "{0}".format(self.header_value)

class Transaction(models.Model):
    transaction = models.BigAutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name ="Transaction"
        verbose_name_plural = "Transactions"
    def __str__(self):
        return "{} {}".format(self.transaction, self.time)
class LogsLog(models.Model):
    name = models.ForeignKey(HeaderName,on_delete=models.CASCADE)
    value = models.ForeignKey(HeaderValue,on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE)
    
    objects = managers.LogsLogManager()
    
    class Meta:
        verbose_name = "LogsLog"
        verbose_name_plural = "LogsLogs"
        unique_together = (("transaction","name"),)
        
    def __str__(self):
         return "{0} {1} {2}".format(self.name, self.value,self.transaction)

class LogsTag(models.Model):
    name_cryteria = models.ForeignKey(HeaderName, on_delete=models.CASCADE)
    value_cryteria = models.TextField()
    tag = models.TextField()
    description = models.TextField()

    class Meta:
        verbose_name = "Logs Tag"
        verbose_name_plural = "Logs Tags"
        ordering = ['id']

    def __str__(self):
        return "{0}".format(self.tag)
    
class LogsTagAssign(models.Model):
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE,to_field="transaction")
    tag = models.ForeignKey(LogsTag,on_delete=models.CASCADE)
    
    objects = managers.LogsTagAssignManager()

    class Meta:
        verbose_name = "Log Tag Assignment"
        verbose_name_plural = "Log Tag Assignments"

    def __str__(self):
        return "{0} {1}".format(self.transaction, self.tag)