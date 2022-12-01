from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',csrf_exempt(views.index)),
    path('newdoc/',csrf_exempt(views.add_doctor)),
    path('newpatient/',csrf_exempt(views.add_patient)),
    path('permission/',csrf_exempt(views.get_permission)),
    path('update/',csrf_exempt(views.update_record)),
    path('addrecord/',csrf_exempt(views.add_record)),
    path('emergency/',csrf_exempt(views.emergency)),
    path('check_sign_in/',csrf_exempt(views.check_sign_in)),
    path('sign_in/',csrf_exempt(views.sign_in)),
    path('add_doc/',csrf_exempt(views.add_doctor_to_patient)),
    path('get_permission/',csrf_exempt(views.get_permission)),
    path('get_file/',csrf_exempt(views.get_file)),
    path('get_all_file/',csrf_exempt(views.acess_all_records)),
    path('generate_otp/',csrf_exempt(views.generate_otp)),
    path('verify_otp/',csrf_exempt(views.verify_otp)),
    path('get_basic_record/',csrf_exempt(views.get_basic_record)),
]
