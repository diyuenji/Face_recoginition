import json
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import os

imageID_path = 'ID_image'
ID_list = []
Total_ID_data={}

#create list of ID image
for filename in os.listdir(imageID_path):
    ID_list.append(cv2.imread(os.path.join(imageID_path,filename)))
# read image
print(ID_list)

for img in ID_list:
    ID_data={}
    reader = easyocr.Reader(['en'], gpu=False)

    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # detect text on image
    text_ = reader.readtext(img)

    threshold = 0.25

    id_num=""
    name=""
    dob=""
    sex=""
    place_of_origin=""
    place_of_residence=""

    state=0
    # draw bbox and text
    for t_, t in enumerate(text_):
        print("-----"+str(t[1]))
        text=t[1]
        if state == 1:
            id_num=text
            state=0
        if state == 2:
            name=text
            state=0
        if state == 3:
            dob=text
            state=0
        if state == 4:
            sex=text
            state=0
        if state == 5 and "residence" not in text:
            place_of_origin+=text
            
        if state == 6:
            place_of_residence+=text
        if " No" in text: 
            state=1
            # print(text)
        elif "Full" in text or "name" in text: state=2
        elif "Date" in text or "birth" in text: 
            state=3 
            print(text)
        elif "Sex" in text: state=4
        elif "origin" in text: state=5
        elif "residence" in text: state=6

        bbox, text, score = t
        # print("---------------------------------"+str(bbox[0][0]))
        if score > threshold:
            cv2.rectangle(img, (int(bbox[0][0]),int(bbox[0][1])),(int(bbox[2][0]),int(bbox[2][1])), (0, 255, 0), 5)
            cv2.putText(img, text, (int(bbox[0][0]),int(bbox[0][1])), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    # print("ID: "+id_num+" Name: "+name+" Birthdate: "+dob+" Sex: "+sex+" Origin: "+place_of_origin+" Residence: "+place_of_residence )
    
    # Add info to each personal data
    ID_data["ID"]=id_num
    ID_data["Name"]=name
    ID_data["Birthdate"]=dob
    ID_data["origin"]=place_of_origin
    Total_ID_data[id_num]=ID_data

# Serializing json
json_object = json.dumps(Total_ID_data, indent=4)
 
# Writing to sample.json
with open("ID_information.json", "w") as outfile:
    outfile.write(json_object)

