import twilio
from twilio.rest import Client
import random # generate random number
account_sid = 'ACc50d92d188482c026b72921e9e6e6860'
auth_token = 'a3171bb7988cb8ec412084faa72c4fe4'
    
def get_otp(request):
    otp = random.randint(1000,9999)
    print("Your OTP is - ",otp)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body='Hello '+request['name']+' Your Secure Device OTP is - ' + str(otp),
            from_='+12055484688',
            to='+91'+request["number"]
        )

    print(message.sid)
    return otp