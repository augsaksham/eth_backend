from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def add_patient(request):
    pass

def add_doctor(request):
    pass

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