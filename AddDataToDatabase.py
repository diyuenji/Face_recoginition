import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facevalidaterealtime-default-rtdb.asia-southeast1.firebasedatabase.app/"
}
)

ref = db.reference("Users")

#load json data
f = open('ID_information.json')
id_data = json.load(f)
f.close()
print(id_data)
#json format we have key and value
data = {
    "080802":{
        "name": "Nhat Quan",
        "id": "0000",
        "birth_year":2002,
        "major":"undegraduate",
        "get-married":"N",
        "last_attendance_time":"2023-12-10 00:54:34"
    },
    "101010":{
        "name": "Messi",
        "id": "0001",
        "birth_year":1987,
        "major":"football player",
        "get-married":"Y",
        "last_attendance_time":"2023-12-10 00:54:34"
    },
    "res":{
        "name": "Ba Dung",
        "id": "0002",
        "birth_year":2002,
        "major":"undegraduate",
        "get-married":'N',
        "last_attendance_time":"2023-12-10 00:54:34"
    },
    "123321":{
        "name": "Bruce Lee",
        "id": "0003",
        "birth_year":1940,
        "major":"martial artist",
        "get-married":"Y",
        "last_attendance_time":"2023-12-10 00:54:34"
    },
    "123456":{
        "name": "Harry Potter",
        "id": "0004",
        "birth_year":1995,
        "major":"wizzard",
        "get-married":"Y",
        "last_attendance_time":"2023-12-10 00:54:34"
    },
}

for key, value in id_data.items():
    ref.child(key).set(value)#send data to specific directory