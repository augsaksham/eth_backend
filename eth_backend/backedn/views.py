from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Doctor,Patient
import uuid  
import json
# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def add_patient(request):
    data = json.loads(request.body.decode("utf-8"))
    id=str(uuid.uuid1().int)
    patient=Patient(id,data['patient_name'],data['patient_adhaar']
                  ,data['patient_wallet'],data['issue_center'])
    patient.save()
    return JsonResponse('Patient Created ID  = '+id, status=201,safe=False)

def add_doctor(request):
    data = json.loads(request.body.decode("utf-8"))
    doctor=Doctor(data['doc_id'],data['doc_name'],data['doc_adhaar']
                  ,data['doc_wallet'],data['issue_center'])
    doctor.save()
    return JsonResponse('True', status=201,safe=False)

def update_record(request):
    pass

def get_permission(request):
    pass

def sign_in_doc(request):
    pass

def sign_in_patient(request):
    pass

def add_record(request):
    pass

def emergency(request):
    pass