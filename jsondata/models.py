from django.db import models
class JsonData(models.Model):
    """Json数据"""
    id = models.AutoField(name='id', primary_key=True)
    data = models.JSONField()
    date_time = models.DateField(auto_now=True)

    class Meta:
        db_table = 'jsondata'
