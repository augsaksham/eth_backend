from logging.config import dictConfig
import os
import requests
from pinatapy import PinataPy
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
gateway="https://ipfs.io/ipfs/"
pinata_api_key=str(os.environ.get('PinataAPIKey'))
pinata_secret_api_key=str(os.environ.get('PinataAPISecret'))
pinata = PinataPy(pinata_api_key,pinata_secret_api_key)
dict_hashes={}

def get_file_hash(filename):
    return dict_hashes[filename]

def check_update_permission():
    return True
    
    
def upload_file(filename,issuer_id="None"):
    
    file_hash = pinata.pin_file_to_ipfs(filename)
    pinata.pin_jobs()
    dict_hashes[filename]=file_hash
    print("Uploaded File")
    return file_hash


def get_file(filename,patient_adhaar="None",issuer_id="None"):
    result=get_file_hash(filename)
    return requests.get(url=gateway+result['IpfsHash']).text


def update_file(filename,patient_adhaar="None",issuer_id="None"):
    
    if(check_update_permission(filename,patient_adhaar,issuer_id)):
        upload_file(filename,issuer_id)
        return True
    else:
        print("Bad Request (Permission Not Granted)")
        return False

upload_file("sample2.json")
print(get_file("sample2.json"))