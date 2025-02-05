import cv2
import face_recognition
import os
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# push image to storage not real time
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facevalidaterealtime-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':"facevalidaterealtime.appspot.com"
}
)


# Import Images
path_img='Images'
imgList=[]
imgID=[]
for path in os.listdir(path_img):
    imgList.append(cv2.imread(os.path.join(path_img,path)))
    imgID.append(os.path.splitext(path)[0])
    
    fileName=f'{path_img}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName) #send fileName
    blob.upload_from_filename(fileName)
# print(imgID)

#opencv use BGR, facerec use RGB
def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        
    return encodeList

print("Encoding started....")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithID=[encodeListKnown,imgID]
print("Encoding finished")

file=open("EncodeFile.p","wb")
pickle.dump(encodeListKnownWithID,file)
file.close()
print("File saved")
