from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Doctor,Patient,Records,File,PatientDoctors,Permissions,Login
import main as mn
import uuid  
import requests
import json
import urllib.parse
# Create your views here.
def index(request):
    return HttpResponse("Hello World")


def handel_file(json_object,id=0):
    #Tested 
    if id==0:
        id=str(uuid.uuid1().int)+'.json'
        with open("files/"+id, "w") as outfile:
            outfile.write(json_object)
    else:
        id+='.json'
        with open("files/"+id, "w") as outfile:
            outfile.write(json_object)
    return id

def add_patient(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    
    try:
        patient=Patient(data['patient_adhaar'],data['patient_name'],data['patient_adhaar']
                    ,data['patient_wallet'],data['issue_center'])
        patient.save()
    except :
        print("Patient Allready Exists")
        return JsonResponse('Patient Allready Exists'+data['patient_name'], status=201,safe=False)
    file=data['file']
    json_object = json.dumps(file)
    file_id=handel_file(json_object)
    file_hash=mn.upload_file(file_id,data['issue_center'])['IpfsHash']
    print("File Hash = ",file_hash)
    fle=File(file_id,file_hash)
    fle.save()
    
    return JsonResponse('Patient Created ID  = '+data['patient_name'], status=201,safe=False)

def add_doctor(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    doctor=Doctor(data['doc_id'],data['doc_name'],data['doc_adhaar']
                  ,data['doc_wallet'],data['issue_center'])
    try:
        doctor.save()
        print("Saved doctor")
    except:
        print("Doc allready Exists ")
        JsonResponse("Doc allready Exists ", status=201,safe=False)
        
    return JsonResponse('True', status=201,safe=False)

def update_record(request):
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    file_id=data["file_id"]
    new_file=data["file"]
    
    if(is_file_of_correct_doc(doc_id,file_id,patient_id)):
        file_hash=File.objects.filter(file_id=file_id).values()[0]["file_hash"]
        json_object = json.dumps(new_file,id=file_id)
        file_id=handel_file(json_object,id=file_id)
        file_hash=mn.upload_file(file_id,doc_id)
        return JsonResponse('True', status=201,safe=False)
    
    else :
        return JsonResponse('Flase', status=201,safe=False)


def get_file(request,request_stat=0):
    #Tested for use serialize json structure
    print("Got request with request state as ",request_stat)
    data={}
    if(request_stat==0):
        data = json.loads(request.body.decode("utf-8"))
    else:
        data=request
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    file_id=data["file_id"]
    if(request_stat>=1 or is_file_of_correct_doc(doc_id,file_id,patient_id)):
        file_hash=File.objects.filter(file_id=file_id).values()[0]["file_hash"]
        print("Requested hash = ",file_hash)
        file=mn.get_file(file_hash)    
        print("Got file as ",file)
        if request_stat==0:
            return JsonResponse({"file":file}, status=201,safe=False)
        else:
            print("*****************************************file***************")
            return file    
            
    else :
        if request_stat==0:
            return JsonResponse({"file":"Error"}, status=201,safe=False)
        else:
            return "Error"   

def is_file_of_correct_doc(doc_id,file_id,patient_id):
    rec=Records.objects.filter(record_id=patient_id+':'+doc_id).values()
    if rec.exists():
        rec=rec[0]["records"]
        files=rec.split(':')
        print("Files list = ",files)
        if file_id in files:
            print("Found file of doctor")
            return True
    print("File not of doctor ")
    return False


def get_permission(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    permission_type=data["type"]
    
    if(permission_type==1):
        rec=Permissions(patient_id+':'+doc_id,"rec")
        rec.save()
        return JsonResponse('Added Permission', status=201,safe=False)
    else :
        #For adding a new Doctor to a Patient
        rec=Permissions(patient_id+':'+doc_id,"add")
        rec.save()
        return JsonResponse('Added Permission', status=201,safe=False)

def acess_all_records(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    result={}
    rec=Permissions.objects.filter(id=patient_id+':'+doc_id).values()
    if rec.exists():
        print("Found Permission")
        doc_ids=PatientDoctors.objects.filter(patient_id=patient_id).values()[0]['doctors'].split(':')
        for doc in doc_ids:
            print("Found doctor name ",doc)
            files=Records.objects.filter(record_id=patient_id+":"+doc).values()
            print("Files query set ",files)
            if not files.exists():
                continue
            else :
                
                files=files[0]['records'].split(':')
                print("Filers are ",files)
                for fl in files:
                    print("Found file name ",fl)
                    req={}
                    req['patient_id']=patient_id
                    req['doc_id']=doc_id
                    req['file_id']=fl
                    json_response={}
                    try:
                        
                        print("Request is ",req)
                        json_response = get_file(req,2)
                    except:
                        print("Error in extracting file id : ",fl)
                        continue
                    if not(json_response=="Error"):
                        continue        
                    else:
                        result[fl]=json_response['file']
        rec=Permissions(patient_id+":"+doc)
        rec.delete()
        return JsonResponse({"Files":result}, status=201,safe=False)
    else:
        return JsonResponse('Permission not granted', status=201,safe=False)
    

def sign_in(request):
    data = json.loads(request.body.decode("utf-8"))
    id=data['id']
    try:
        rec=Login(id,"True")
        rec.save()
    except:
        print("Allready Signed in ")
    return JsonResponse('Signed In', status=201,safe=False)
    


def check_sign_in(request):
    data = json.loads(request.body.decode("utf-8"))
    id=data['id']
    sign_in_status='False'
    try:
        sign_in_status=Login.objects.filter(id=id).values()[0]['status']
    except:
        sign_in_status='False'
    return JsonResponse(sign_in_status, status=201,safe=False)

        

    

def add_doctor_to_patient(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    rec=Permissions.objects.filter(id=patient_id+':'+doc_id).values()
    if rec.exists():
        print("Found rec")
        docs=PatientDoctors.objects.filter(patient_id=patient_id).values()
        if docs.exists():
            docs=docs[0]
            if doc_id in docs['doctors']:
                return JsonResponse('Doc Allready Exists', status=201,safe=False)

            docs["doctors"]+=(":"+doc_id)
            new_rec=PatientDoctors(patient_id,docs["doctors"])
            new_rec.save()
        else:
            new_rec=PatientDoctors(patient_id,doc_id)
            new_rec.save()
        new_rec=Permissions(id=patient_id+':'+doc_id)
        new_rec.delete()
        return JsonResponse('Added Doctor', status=201,safe=False)
    else:
        return JsonResponse('Permission Denied', status=201,safe=False)
        
    
def add_record(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    doc_id=data['doc_id']
    patient_id=data['patient_id']
    record_id=patient_id+':'+doc_id
    file=data['file']
    doc_record=PatientDoctors.objects.filter(patient_id=patient_id).values()
    if doc_record.exists():
        print("Doctor Previously Added Addind Record")
        json_object = json.dumps(file)
        file_id=handel_file(json_object)
        file_hash=mn.upload_file(file_id,data['issue_center'])['IpfsHash']
        record=Records.objects.filter(record_id=record_id).values()
        if record.exists():
            print("Find previous Records")
            record=record[0]
            record["records"]+=(":"+file_id)
            rec=Records(record_id,record["records"])
            rec.save()
        else:
            print("Made new Record")
            rec=Records(record_id,file_id[0:file_id.find('.')])
            rec.save()
        fle=File(file_id[0:file_id.find('.')],file_hash)
        fle.save()
        print("Saved file")
    else:
        return JsonResponse('Doctor not added to patient', status=201,safe=False)
    return JsonResponse('True', status=201,safe=False)

def emergency(request):
    pass