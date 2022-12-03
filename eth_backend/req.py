import requests
import json

# req_data={"id":"6654635644",
#     "doc_id":"123456789",
#     "otp":"5518",
#     "number":"7661835084",
#     "date":"20/02/2002",
#     "doc_name":"ramesh",
#     "doc_adhaar":"123456789789",
#     "doc_wallet":"5465654idjsd",
#     "file_id":"304019077147405513271530110209682668898",
#     "type":"2",
#     "patient_id":"123456789",
#     "patient_name":"idjsd sdfgf",
#     "patient_adhaar":"123456789",
#     "patient_wallet":"5465654idjsd",
#     "issue_center":"sdfdfs44idjsd",
#     "file":{"fruit": "Apple",
#         "size": "Largkkke",
#         "color": "Red",
#         "frruit": "Applejjjjj",
#         "sirze": "Large",
#         "corlor": "Red",
#         "huehue":"jhkdfkd"
#     }}

# rs={"id": "6654635644", "doc_id": "123456789", "otp": "5518", "number": "7661835084", "date": "20/02/2002", "doc_name": "ramesh", "doc_adhaar": "123456789789", "doc_wallet": "5465654idjsd", "file_id": "304019077147405513271530110209682668898", "type": "2", "patient_id": "123456789", "patient_name": "idjsd sdfgf", "patient_adhaar": "123456789", "patient_wallet": "5465654idjsd", "issue_center": "sdfdfs44idjsd", "file": {"fruit": "Apple", "size": "Largkkke", "color": "Red", "frruit": "Applejjjjj", "sirze": "Large", "corlor": "Red", "huehue": "jhkdfkd"}}
# req_data = json.dumps(req_data)
# print(req_data)
# response1 = requests.post('http://127.0.0.1:8000/get_file/', req_data)
# print(response1.text)
dta="{id: 6654635644, doc_id: 123456789, otp: 5518, number: 7661835084, date: 20/02/2002, doc_name: ramesh, doc_adhaar: 123456789789, doc_wallet: 5465654idjsd, file_id: 304019077147405513271530110209682668898, type: 2, patient_id: 123456789, patient_name: idjsdsdfgf, patient_adhaar: 123456789, patient_wallet: 5465654idjsd, issue_center: sdfdfs44idjsd, file: {fruit: Apple, size: Largkkke, color: Red, frruit: Applejjjjj, sirze: Large, corlor: Red, huehue: jhkdfkd}}"

print(dta)
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

re=convert_to_dict(dta)

js=json.loads(re)
print(js)
print("Type = ",type(js))