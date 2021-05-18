from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
'''
class tblLiner(models.Model):
    ModelName = models.CharField(max_length=100,db_column='ModelName')
    FullName = models.CharField(max_length=100)
    DateJoined = models.DateField()
#    card_status = models.IntegerField()
#    card_serial_no = models.IntegerField()
    ShiftPatternId=models.CharField(max_length=100,db_column='ShiftPatternId')
    class Meta:
        db_table = 'tblLiner'
        managed = False

UnitSize
OrderCode
LinerType
LinerAddIDRad
LinerAddIDDisch
Option
Active

'''

class airflow(models.Model):
    size_inch = models.CharField(max_length=7,primary_key=True,db_column='size_inch')
    cfm_min = models.IntegerField(db_column='cfm_min')
    cfm_max = models.IntegerField(db_column='cfm_max')
    class Meta:
        db_table = 'airflow'
        managed = False

class performance(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    size_inch = models.CharField(max_length=5, db_column='size_inch')
    cfm = models.IntegerField(db_column='cfm')
    discharge_nr = models.IntegerField(db_column='discharge_nr')
    radiated_nr = models.IntegerField(db_column='radiated_nr')
    class Meta:
        db_table = 'performance'
        managed = False

