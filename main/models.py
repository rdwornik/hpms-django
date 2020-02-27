from django.db import models

# Create your models here.

class HeaderName(models.Model):
    header_name = models.TextField(unique=True)
    def __str__(self):
        return "{0} {1}".format(self.id, self.header_name)

class HeaderValue(models.Model):
    header_value = models.TextField(unique=True)
    header_names = models.ManyToManyField(HeaderName, through="LogsLog")

    def __str__(self):
        return "{0} {1}".format(self.id ,self.header_value)

class LogsLog(models.Model):
    transaction = models.BigIntegerField(default=1)
    name = models.ForeignKey(HeaderName,on_delete=models.CASCADE)
    value = models.ForeignKey(HeaderValue,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Logs Log'
        verbose_name_plural = 'Logs Log'
        get_latest_by = 'transaction'
    def __str__(self):
        return "{0} {1} {2}".format(self.transaction,self.name, self.value)