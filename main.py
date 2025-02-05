import cv2
import os
import face_recognition
import pickle
import numpy as np
import cvzone
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

bucket=storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640)#thông số của x cam
cap.set(4,480)#thông số của y cam

#Background
imgBackGround = cv2.imread("Resources/Background.png")
#Frame
imgFrame=cv2.imread("Resources/frame.png")

#Import mode
path_mode='Resources/Modes'
imgModesList=[]
for path in os.listdir(path_mode):
    imgModesList.append(cv2.imread(os.path.join(path_mode,path)))

# Load Encoding Files
print("Loading Encoding Files...") 
file=open("EncodeFile.p","rb")
encodeListKnownWithID=pickle.load(file)
file.close()
encodeListKnown,imgID=encodeListKnownWithID
print("Encode Files Loaded") 


#variables
counter=0
id=-1
modeType=0

while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)
    
    imgSmall =cv2.resize(img,(0,0),None,0.25,0.25)#rescale to reduce computation
    imgSmall=cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
    
    faceCurFrame=face_recognition.face_locations(imgSmall)#Face location
    encodeCurFrame=face_recognition.face_encodings(imgSmall,faceCurFrame)#to compare data vs reality
    
    #Overlay webcam and background
    h,w,_=imgModesList[1].shape
    imgBackGround[150:150+480,61:61+640]=img #original point at top left rectangle
    imgBackGround[0:h,750:750+w]=imgModesList[modeType] #start and end point of overlap
    # imgBackGround[180:180+480,55:55+640]=img[1] 
    # imgBackGround[180:180+480,55:55+640]=img[2] 
    # imgBackGround[180:180+480,55:55+640]=img[3] 
    
    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):#Zip to combine 2 loops to 1 loops
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)#boolen if matches
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)#distance lower is better( it means may have more than 1 True img)
        # print("Matches\n",matches,"Face distance",faceDis)
        
        matchIndex=np.argmin(faceDis)#index of true match
        if matches[matchIndex]:
            # print("Known Face Detected")
            print(imgID[matchIndex])
            # cv2.rectangle(imgID[matchIndex],)
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1*4 ,x2*4 ,y2*4 ,x1*4
            bbox=55+x1,140+y1, x2-x1, y2-y1
            imgBackGround=cvzone.cornerRect(imgBackGround,bbox,rt=0)#rt= rectangle thickness, rect detect face
            id=imgID[matchIndex]
            
            if(counter==0):
                cvzone.putTextRect(imgBackGround,"Loading",(275,400))
                cv2.imshow("Face Recog",imgBackGround)
                cv2.waitKey(1)
                counter=1
                modeType=1
    
    if(counter!=0):
        if(counter==1):
            #Get data from firebase
            userInfo = db.reference(f'Users/{id}').get()
            print(userInfo)
            #Get image from firebase
            blob =bucket.get_blob(f'Images/{id}.png')
            array=np.frombuffer(blob.download_as_string(),np.uint8)
            imgUser=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
            #Update data
            # ref=db.reference(f'Users/{id}')
            # userInfo["var_change"]+=1
            # ref.child("var_change").set_value(userInfo["var_change"])
        
        if 100< counter<=150:
            modeType=2
            imgBackGround[150:150+480,61:61+640]=img #update or delete previous thing apear on
            
        
        
        if counter<=100:    
            cv2.putText(imgBackGround,str(userInfo['id']),(800,485),cv2.FONT_HERSHEY_DUPLEX ,0.7,(105,105,105),1)
            cv2.putText(imgBackGround,str(userInfo['major']),(800,590),cv2.FONT_HERSHEY_DUPLEX ,0.7,(105,105,105),1)
            cv2.putText(imgBackGround,str(userInfo['birth_year']),(880,665),cv2.FONT_HERSHEY_DUPLEX ,0.7,(0,0,0),1)
            cv2.putText(imgBackGround,str(userInfo['get-married']),(1095,665),cv2.FONT_HERSHEY_DUPLEX ,0.7,(0,0,0),1)
            
            (w, h), _=cv2.getTextSize(userInfo['name'],cv2.FONT_HERSHEY_DUPLEX ,1,1)
            offset = int((450-w)/2)
            cv2.putText(imgBackGround,str(userInfo['name']),(750+offset,400),cv2.FONT_HERSHEY_DUPLEX ,1,(105,105,105),1)
            
            
            imgBackGround[88:88+216,868:868+216]=imgUser
        counter+=1
        
        if counter>150:
            counter=0
            modeType=0
            userInfo=[]
            imgUser=[]
            imgBackGround[150:150+480,61:61+640]=img #update or delete previous thing apear on
    
    # cv2.imshow("Webcam",img) #Name of UI
    cv2.imshow("Face Recog",imgBackGround)
    # cv2.waitKey(1)#milisecond
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break
cv2.destroyAllWindows() 
