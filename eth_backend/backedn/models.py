from django.db import models


# Create your models here.

class Doctor(models.Model):
    doc_id=models.CharField(max_length=50,primary_key=True)
    doc_name=models.CharField(max_length=100)
    doc_adhaar=models.CharField(max_length=15)
    doc_wallet=models.CharField(max_length=50)
    issue_center=models.CharField(max_length=50)
    
    
class Patient(models.Model):
    
    patient_id=models.CharField(max_length=15,primary_key=True,default="None")
    patient_name=models.CharField(max_length=100)
    patient_adhaar=models.CharField(max_length=15)
    patient_wallet=models.CharField(max_length=50)
    issue_center=models.CharField(max_length=50)


class Records(models.Model):
    record_id=models.CharField(max_length=100,primary_key=True)
    records=models.TextField()
    
class File(models.Model):
    file_id=models.CharField(max_length=100,primary_key=True)
    file_hash=models.CharField(max_length=100)
    
    
class PatientDoctors(models.Model):
    patient_id=models.CharField(max_length=50,primary_key=True,default="None")
    doctors=models.TextField()
    
    
class Permissions(models.Model):
    id=models.CharField(max_length=100,primary_key=True,default="None")
    premission_type=models.CharField(max_length=5)
    
class Login(models.Model):
    id=models.CharField(max_length=100,primary_key=True,default="None")
    status=models.CharField(max_length=5)
    
class Emergency(models.Model):
    id=models.CharField(max_length=100,primary_key=True,default="None")
    date=models.CharField(max_length=15)
    
    
class Mobile(models.Model):
    id=models.CharField(max_length=50,primary_key=True,default="None")
    name=models.CharField(max_length=50)
    number=models.CharField(max_length=15)
    
class Otp(models.Model):
    id=models.CharField(max_length=50,primary_key=True,default="None")
    otp=models.CharField(max_length=10)
    