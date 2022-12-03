from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Doctor,Patient,Records,File,PatientDoctors,Permissions,Login,Emergency,Mobile,Otp
import main as mn
import get_otp
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
    file_id=handel_file(json_object,"basic_record"+data["patient_adhaar"])
    file_hash=mn.upload_file(file_id,data['issue_center'])['IpfsHash']
    print("File Hash = ",file_hash)
    fle=File(file_id,file_hash)
    fle.save()
    mob=Mobile(data['patient_adhaar'],data['patient_name'],data['number'])
    mob.save()
    
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
    mob=Mobile(data['doc_id'],data['doc_name'],data['number'])
    mob.save()    
    return JsonResponse('True', status=201,safe=False)

def give_file(file_hash):
    f = open('files/'+file_hash+'.json')
    data = json.load(f)
    return data


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

def convert_to_dict(inp):
    i=0
    while i<(len(inp)-1):
        # if i>=100:
        #     return inp
        if(inp[i]=='{'):
            # print("Found at 1 i = ",i)
            # print("P1 = ",inp[0:i+1])
            # print("P2 = ",inp[i+1:])
            ip=inp[0:i+1]+"\""+inp[i+1:]
            # print("Final Result = ************ = ",ip)
            inp=ip
            i+=1
        elif (inp[i]==':'and not(inp[i-1]=="\"")):
            print("Found at 2 i = ",i)
            print("P1 = ",inp[0:i])
            print("P2 = ",inp[i:])
            ip=inp[0:i]+"\""+inp[i:]
            print("Final Result = ************ = ",ip)
            i+=1
            inp=ip
        elif (inp[i]==" " and not(inp[i+1]=='{')):
            # print("Found at i 3 = ",i)
            # print("P1 = ",inp[0:i+1])
            # print("P2 = ",inp[i+1:])
            ip=inp[0:i+1]+"\""+inp[i+1:]
            # print("Final Result = ************ = ",ip)
            i+=1
            inp=ip
        elif(inp[i]=="," ):
            # print("Found at i 4 = ",i)
            # print("P1 = ",inp[0:i])
            # print("P2 = ",inp[i:])
            ip=inp[0:i]+"\""+inp[i:]
            # print("Final Result = ************ = ",ip)
            i+=1
            inp=ip
        elif(inp[i]=="}" and not(inp[i-1]=="}") ):
            # print("Found at i 5 = ",i)
            # print("P1 = ",inp[0:i])
            # print("P2 = ",inp[i:])
            ip=inp[0:i]+"\""+inp[i:]
            # print("Final Result = ************ = ",ip)
            i+=1
            inp=ip
        i+=1
    return inp

def get_file(request,request_stat=0):
    print("************** Got Request as ************* ",request)
    #Tested for use serialize json structure
    print("Got request with request state as ",request_stat)
    data={}
    if(request_stat==0):
        data = json.loads(request.body.decode("utf-8"))
    else:
        data=request
    print("********** Got Data As ***************",data)
    print("tyoe data = ",type(data))
    if(str(type(data))=="<class 'str'>"):
        print("Data is String converting to JSON")
        data=json.loads(convert_to_dict(data))
    
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    file_id=data["file_id"]
    if(request_stat>=1 or is_file_of_correct_doc(doc_id,file_id,patient_id)):
        file_hash=File.objects.filter(file_id=file_id).values()[0]["file_hash"]
        print("Requested hash = ",file_hash)
        # file=mn.get_file(file_hash)    
        file=give_file(file_id)
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
    #Tested
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

def generate_otp(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    id=data["patient_id"]
    rec=Mobile.objects.filter(id=id).values()[0]
    rec=Otp(id,get_otp.get_otp(rec))
    rec.save()
    return JsonResponse("Otp Sent", status=201,safe=False)

def verify_otp(request):
    #Tested
    data = json.loads(request.body.decode("utf-8"))
    id=data["patient_id"]
    input_otp=data["otp"]
    correct_otp=Otp.objects.filter(id=id).values()[0]['otp']
    if (correct_otp==input_otp):
        rec=Otp(id=id)
        rec.delete()
        return JsonResponse("True", status=201,safe=False)
    else :
        return JsonResponse("False", status=201,safe=False)

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

def acess_all_records(request,admin=0):
    #Tested
    data={}
    if admin==0:
        data = json.loads(request.body.decode("utf-8"))
    else :
        data=request
        
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    result={}
    rec=Permissions.objects.filter(id=patient_id+':'+doc_id).values()
    if admin==1 or rec.exists():
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
                        print("Got Response as ",json_response)
                    except:
                        print("Error in extracting file id : ",fl)
                        continue
                    if (json_response=="Error"):
                        continue        
                    else:
                        result[fl]=json_response
        rec=Permissions(patient_id+":"+doc)
        rec.delete()
        
        if admin==0:
            return JsonResponse({"Files":result}, status=201,safe=False)
        else :
            return result
    else:
        if admin==0:
            return JsonResponse({"Files":'Permission not granted'}, status=201,safe=False)
        else :
            return "Permission Not Granted"
    

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
        print("Json Object = ",json_object)
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
    #Can be used for 2 purpose use doc_id==patient_id to acess all records of patient without logging the acess
    data = json.loads(request.body.decode("utf-8"))
    patient_id=data["patient_id"]
    doc_id=data["doc_id"]
    id=patient_id+":"+doc_id
    req={}
    req["patient_id"]=data["patient_id"]
    req["doc_id"]=data["doc_id"]
    try:
        rec=Permissions(patient_id+':'+doc_id,"rec")
        rec.save()
    except:
        pass
    if not(patient_id==doc_id) :#check is patient is trying to acess his information
        try:
            date=data["date"]
            rec=Emergency(id,date)
            rec.save()
        except:
            rec=Emergency(id=id)
            rec.delete()
            date=data["date"]
            rec=Emergency(id,date)
            rec.save()
    else:
        print("Patient Acessing his information")
        pass
    return JsonResponse({"Files":acess_all_records(req,admin=1)}, status=201,safe=False)
    
def get_basic_record(request):
    data = json.loads(request.body.decode("utf-8"))
    return JsonResponse({"File":give_file("basic_record"+data['patient_id'])}, status=201,safe=False)
