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
    id = models.AutoField(primary_key=True, db_column='id')
    user = models.IntegerField(db_column='user_id')
    quantity = models.IntegerField(db_column='quantity')
    size = models.CharField(max_length=10, db_column='size')
    design_airflow = models.IntegerField(db_column='design_airflow')
    min_airflow = models.IntegerField(db_column='min_airflow')
    attenuator = models.CharField(max_length=5, db_column='attenuator')
    outlet_type = models.CharField(max_length=150, db_column='outlet_type')
    insulation = models.CharField(max_length=100, db_column='insulation')
    controls = models.CharField(max_length=255, db_column='controls')
    vav_size = models.CharField(max_length=10, db_column='vav_size')
    dNR = models.IntegerField(db_column='dNR')
    rNR = models.IntegerField(db_column='rNR')
    d125 = models.IntegerField(db_column='d125')
    d250 = models.IntegerField(db_column='d250')
    d500 = models.IntegerField(db_column='d500')
    d1000 = models.IntegerField(db_column='d1000')
    d2000 = models.IntegerField(db_column='d2000')
    d4000 = models.IntegerField(db_column='d4000')
    r125 = models.IntegerField(db_column='r125')
    r250 = models.IntegerField(db_column='r250')
    r500 = models.IntegerField(db_column='r500')
    r1000 = models.IntegerField(db_column='r1000')
    r2000 = models.IntegerField(db_column='r2000')
    r4000 = models.IntegerField(db_column='r4000')
    project = models.IntegerField(db_column='project_id')
    product = models.IntegerField(db_column='product_id')
    cfm = models.IntegerField(db_column='cfm')

    class Meta:
        db_table = 'cart'
        managed = False

class project_info(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    project_name = models.CharField(max_length=255, db_column='project_name')
    project_number = models.CharField(max_length=255,db_column='project_number')
    user = models.IntegerField(db_column='user_id')
    project_date = models.DateField(db_column='project_date')
    location = models.CharField(max_length=255, db_column='location')
    city = models.CharField(max_length=255, db_column='city')
    state = models.CharField(max_length=255, db_column='state')
    engineer = models.CharField(max_length=255, db_column='engineer')
    client_name = models.CharField(max_length=255, db_column='client_name')
    consultant_name = models.CharField(max_length=255, db_column='consultant_name')
    prepared_by = models.CharField(max_length=255, db_column='prepared_by')
    remarks = models.CharField(max_length=255, db_column='remarks')
   # created_at = models.DateField(db_column='created_at',default=datetime.now())

    class Meta:
        db_table = 'project_info'
        managed = False

class user_project_mapping(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    user = models.IntegerField(db_column='user_id')
    project = models.IntegerField(db_column='project_id')

    class Meta:
        db_table = 'user_project_mapping'
        managed = False