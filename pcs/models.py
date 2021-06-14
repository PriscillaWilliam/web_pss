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

class discharge_acoustic_data(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    size_inch = models.CharField(max_length=5, db_column='size_inch')
    cfm = models.IntegerField(db_column='cfm')
    Hz125 = models.IntegerField(db_column='125')
    Hz250 = models.IntegerField(db_column='250')
    Hz500 = models.IntegerField(db_column='500')
    Hz1000 = models.IntegerField(db_column='1000')
    Hz2000 = models.IntegerField(db_column='2000')
    Hz4000 = models.IntegerField(db_column='4000')
    NR = models.IntegerField(db_column='NR')
    class Meta:
        db_table = 'discharge_acoustic_data'
        managed = False

class radiated_acoustic_data(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    size_inch = models.CharField(max_length=5, db_column='size_inch')
    cfm = models.IntegerField(db_column='cfm')
    Hz125 = models.IntegerField(db_column='125')
    Hz250 = models.IntegerField(db_column='250')
    Hz500 = models.IntegerField(db_column='500')
    Hz1000 = models.IntegerField(db_column='1000')
    Hz2000 = models.IntegerField(db_column='2000')
    Hz4000 = models.IntegerField(db_column='4000')
    NR = models.IntegerField(db_column='NR')
    class Meta:
        db_table = 'radiated_acoustic_data'
        managed = False

class cart(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(db_column='quantity')
    size = models.CharField(max_length=10, db_column='size')
    class Meta:
        db_table = 'cart'
        managed = False