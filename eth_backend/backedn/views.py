from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Doctor,Patient
import main as mn
import uuid  
import json
# Create your views here.
def index(request):
    return HttpResponse("Hello World")


def handel_file(json_object):
    id=str(uuid.uuid1().int)
    with open("files/"+id, "w") as outfile:
        outfile.write(json_object)
    return id

def add_patient(request):
    data = json.loads(request.body.decode("utf-8"))
    id=str(uuid.uuid1().int)
    patient=Patient(id,data['patient_name'],data['patient_adhaar']
                  ,data['patient_wallet'],data['issue_center'])
    patient.save()
    file=data['file']
    json_object = json.dumps(file)
    file_id=handel_file(json_object)
    file_hash=mn.upload_file(file_id,data['issue_center'])
    
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
    data = json.loads(request.body.decode("utf-8"))
    doc_id=data['doc_id']
    patient_id=data['patient_id']
    file=data['file']
    
    json_object = json.dumps(file)
    file_id=handel_file(json_object)
    file_hash=mn.upload_file(file_id,data['issue_center'])
    
    pass

def emergency(request):
    pass