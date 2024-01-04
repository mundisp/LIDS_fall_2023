# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class Alert(models.Model):
#     time= models.CharField(max_length=100)
#     pLength= models.CharField(max_length=100)
#     dstIp= models.CharField(max_length=100)
#     srcIP= models.CharField(max_length=100)
#     dstPort= models.CharField(max_length=100)
#     srcPort= models.CharField(max_length=100)
#     protocol= models.CharField(max_length=100)
#     severity= models.CharField(max_length=100)
#     reason= models.CharField(max_length=100)
#     info= models.CharField(max_length=500)
#     filename= models.CharField(max_length=100)

class Alert(models.Model):
    alert_id = models.AutoField(primary_key=True, blank=False, null=False)
    severity_level = models.CharField(blank=True, null=True,max_length=100)
    time = models.CharField(blank=True, null=True,max_length=500)  # This field type is a guess.
    ip_src = models.CharField(blank=True, null=True,max_length=100)
    port_src = models.CharField(blank=True, null=True,max_length=100)
    ip_dst = models.CharField(blank=True, null=True,max_length=100)
    port_dst = models.CharField(blank=True, null=True,max_length=100)
    length = models.CharField(blank=True, null=True,max_length=100)
    protocol = models.CharField(blank=True, null=True,max_length=100)
    reason = models.CharField(blank=True, null=True,max_length=500)
    filename = models.CharField(blank=True, null=True,max_length=100)

    class Meta:
        managed = False
        db_table = 'alerts'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DashboardAlert(models.Model):
    time = models.CharField(max_length=100)
    plength = models.CharField(db_column='pLength', max_length=100)  # Field name made lowercase.
    dstip = models.CharField(db_column='dstIp', max_length=100)  # Field name made lowercase.
    srcip = models.CharField(db_column='srcIP', max_length=100)  # Field name made lowercase.
    dstport = models.CharField(db_column='dstPort', max_length=100)  # Field name made lowercase.
    srcport = models.CharField(db_column='srcPort', max_length=100)  # Field name made lowercase.
    protocol = models.CharField(max_length=100)
    severity = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    info = models.CharField(max_length=500)
    filename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'dashboard_alert'


class DashboardEmployee(models.Model):
    empid = models.IntegerField(db_column='Empid')  # Field name made lowercase.
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    salary = models.IntegerField()
    department = models.CharField(db_column='Department', max_length=25)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dashboard_employee'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



# Create your models here.
# class Employee(models.Model):
#     Empid= models.IntegerField()
#     name= models.CharField(max_length=25)
#     address= models.CharField(max_length=100)
#     salary= models.IntegerField()
#     Department= models.CharField(max_length=25)
#

