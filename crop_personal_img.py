from ultralytics import YOLO
from PIL import Image
import cv2
import os

imageid_path = "ID_image"
output_path  = "ImageRaw"
imgList=[]

model=YOLO("yolov8n.pt")

for filename in os.listdir(imageid_path):
    imgList.append(filename)
    print(imgList)



for filename in imgList:
    image_path=os.path.join(imageid_path,filename)
    results=model.predict(source=image_path)
    for r in results:  # View facial detection of your ID card
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.show()  # show image
    
    class_names = model.names    
    for r in results:
        for box in r.boxes:
            if(int(box.cls[0])==0):  # label of "person" in yolov8
                boxes = box  # Boxes object for bbox outputs
                x_topleft, y_topleft = int(boxes.xyxy[0][0]), int(boxes.xyxy[0][2])
                x_botright, y_botright = int(boxes.xyxy[0][1]), int(boxes.xyxy[0][3])
            else:
                print("Can not detect facial image in ID card")
        
    image=cv2.imread(image_path)

    crop_image = image[y_topleft:y_botright,x_topleft:x_botright] # height, width
    cv2.imwrite(os.path.join(output_path,filename), crop_image)
 
 