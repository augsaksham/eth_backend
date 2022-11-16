from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',csrf_exempt(views.index)),
    path('newdoc/',csrf_exempt(views.add_doctor)),
    path('newpatient/',csrf_exempt(views.add_patient)),
    path('permission/',csrf_exempt(views.get_permission)),
    path('update/',csrf_exempt(views.update_record)),
    path('signindoc/',csrf_exempt(views.sign_in_doc)),
    path('signinpatient/',csrf_exempt(views.sign_in_patient)),
    path('addrecord/',csrf_exempt(views.add_record)),
    path('emergency/',csrf_exempt(views.emergency)),

]
