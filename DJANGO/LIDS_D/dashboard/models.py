from django.db import models

# Create your models here.

class Employee(models.Model):
    Empid= models.IntegerField()
    name= models.CharField(max_length=25)
    address= models.CharField(max_length=100)
    salary= models.IntegerField()
    Department= models.CharField(max_length=25)

class Alert(models.Model):
    alert_id= models.CharField(max_length=100)
    severity_level= models.CharField(max_length=100)
    time= models.CharField(max_length=100)
    ip_src= models.CharField(max_length=100)
    port_src= models.CharField(max_length=100)
    ip_dst= models.CharField(max_length=100)
    port_dst= models.CharField(max_length=100)
    length= models.CharField(max_length=100)
    protocol= models.CharField(max_length=100)
    descripton= models.CharField(max_length=500)
    info= models.CharField(max_length=500)
    filename = models.CharField(max_length=100)
    user_id= models.CharField(max_length=999)