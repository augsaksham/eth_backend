from django.db import models

# Create your models here.

class Doctor(models.Model):
    doc_id=models.CharField(max_length=50,primary_key=True)
    doc_name=models.CharField(max_length=100)
    doc_adhaar=models.CharField(max_length=15)
    doc_wallet=models.CharField(max_length=50)
    issue_center=models.CharField(max_length=50)
    
    
class Patient(models.Model):
    patient_id=models.CharField(max_length=50,primary_key=True,default="None")
    patient_name=models.CharField(max_length=100)
    patient_adhaar=models.CharField(max_length=15)
    patient_wallet=models.CharField(max_length=50)
    issue_center=models.CharField(max_length=50)
