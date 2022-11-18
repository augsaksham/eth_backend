from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Doctor,Patient,Records,File,PatientDoctors,Permissions
import main as mn
import uuid  
import json
# Create your views here.
def index(request):
    return HttpResponse("Hello World")


def handel_file(json_object,id=0):
    if id==0:
        id=str(uuid.uuid1().int)
        with open("files/"+id, "w") as outfile:
            outfile.write(json_object)
    else:
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
    fle=File(file_id,file_hash)
    fle.save()
    
    return JsonResponse('Patient Created ID  = '+id, status=201,safe=False)

def add_doctor(request):
    data = json.loads(request.body.decode("utf-8"))
    doctor=Doctor(data['doc_id'],data['doc_name'],data['doc_adhaar']
                  ,data['doc_wallet'],data['issue_center'])
    doctor.save()
    return JsonResponse('True', status=201,safe=False)

def update_record(request):
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    file_id=data["file_id"]
    new_file=data["file"]
    
    if(is_file_of_correct_doc(doc_id,file_id,patient_id)):
        file_hash=File.objects.filter(file_id=file_id).values()["file_hash"]
        json_object = json.dumps(new_file,id=file_id)
        file_id=handel_file(json_object)
        file_hash=mn.upload_file(file_id,doc_id)
        return JsonResponse('True', status=201,safe=False)
    
    else :
        return JsonResponse('Flase', status=201,safe=False)


def get_file(request):
    #To get a specific file specify url
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    file_id=data["file_id"]
    if(is_file_of_correct_doc(doc_id,file_id,patient_id)):
        file_hash=File.objects.filter(file_id=file_id).values()["file_hash"]
        file=mn.get_file(file_hash)        
        return JsonResponse(file, status=201,safe=False)
    else :
        return JsonResponse('Flase', status=201,safe=False)
        

def is_file_of_correct_doc(doc_id,file_id,patient_id):
    rec=Records.objects.filter(record_id=patient_id+':'+doc_id).values()["records"]
    if not(rec==None):
        files=rec.split(':')
        if file_id in files:
            return True
    return False


def get_permission(request):
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    permission_type=data["type"]
    
    if(permission_type==1):
        # For acessing Records
        pass
    else :
        #For adding a new Doctor to a Patient
        pass
        
    
    pass

def acess_all_records(request):
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    rec=Permissions.objects.filter(id=patient_id+':'+doc_id).values()
    if not(rec==None):
        doc_ids=PatientDoctors.objects.filter(patient_id=patient_id).values()['doctors'].split(':')
        for doc in doc_ids:
            files=record=Records.objects.filter(record_id=patient_id+":"+doc_id).values()['records'].split(':')
            for fl in files:
                req={}
                req['patient_id']=patient_id
                req['doc_id']=doc_id
                req['file_id']=fl
                #Make request to get file 
        return JsonResponse('True', status=201,safe=False)
    else:
        return JsonResponse('False', status=201,safe=False)
    

def sign_in_doc(request):
    pass

def sign_in_patient(request):
    pass

def add_doctor_to_patient(request):
    #Pending URL
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    rec=Permissions.objects.filter(id=patient_id+':'+doc_id).values()
    if not(rec==None):
        docs=PatientDoctors.objects.filter(patient_id=patient_id).values()
        if not(docs==None):
            docs["doctors"]+=(":"+doc_id)
            new_rec=PatientDoctors(patient_id,docs["doctors"])
            new_rec.save()
        else:
            new_rec=PatientDoctors(patient_id,doc_id)
            new_rec.save()
        new_rec=Permissions(id=patient_id+':'+doc_id)
        new_rec.delete()
        return JsonResponse('True', status=201,safe=False)
    else:
        return JsonResponse('False', status=201,safe=False)
        
    
def add_record(request):
    
    data = json.loads(request.body.decode("utf-8"))
    doc_id=data['doc_id']
    patient_id=data['patient_id']
    record_id=patient_id+':'+doc_id
    file=data['file']
    json_object = json.dumps(file)
    file_id=handel_file(json_object)
    file_hash=mn.upload_file(file_id,data['issue_center'])
    record=Records.objects.filter(record_id=record_id).values()
    if not(record==None):
        record["records"]+=(":"+file_id)
        rec=Records(record_id,record["records"])
        rec.save()
    else:
        rec=Records(record_id,file_hash)
        rec.save()
    fle=File(file_id,file_hash)
    fle.save()
    return JsonResponse('True', status=201,safe=False)

def emergency(request):
    pass