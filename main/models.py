
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
    
class LogsLog(models.Model):
    transaction = models.BigIntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)
    name = models.ForeignKey(HeaderName,on_delete=models.CASCADE)
    value = models.ForeignKey(HeaderValue,on_delete=models.CASCADE)
        
    objects = managers.LogsLogManager()

    class Meta:
        verbose_name = "Logs Log"
        verbose_name_plural = "Logs Log"
        get_latest_by = "transaction"
    def __str__(self):
        return "{0} | {1} | {2} | {3}".format(self.transaction,
                                                    self.name, 
                                                    self.value,
                                                    self.time)
      
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
    transaction = models.IntegerField()
    tag = models.ForeignKey(LogsTag,on_delete=models.CASCADE)
    
    objects = managers.LogsTagAssignManager()

    class Meta:
        verbose_name = "Logs Tag Assign"
        verbose_name_plural = "Logs Tags Assign"

    def __str__(self):
        return "{0} {1}".format(self.transaction, self.tag)