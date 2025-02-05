from ultralytics import YOLO
from PIL import Image
import cv2
import os

imageid_path = "ID_image"
output_path  = "ImageRaw"
imgList=[]

model1=YOLO("yolov8n.pt")

for filename in os.listdir(imageid_path):
    imgList.append(filename)
    print(imgList)



for filename in imgList:
    image_path=os.path.join(imageid_path,filename)
    results1=model1.predict(source=image_path)
    # for r in results1:
    #     im_array = r.plot()  # plot a BGR numpy array of predictions
    #     im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    #     im.show()  # show image
        
    for r in results1:
            boxes = r.boxes  # Boxes object for bbox outputs
            masks = r.masks  # Masks object for segment masks outputs
            probs = r.probs  # Class probabilities for classification outputs
            # print(boxes)
    print("axis")
    print(boxes.xyxy[0][0],boxes.xyxy[0][1],boxes.xyxy[0][2],boxes.xyxy[0][3]) # print       
    image=cv2.imread(image_path)

    # im1 = im.crop((left, top, right, bottom))
    crop_image = image[int(boxes.xyxy[0][2]):int(boxes.xyxy[0][3]),int(boxes.xyxy[0][0]):int(boxes.xyxy[0][1])]
    # im1 = im.crop((int(boxes.xyxy[0][0]),int(boxes.xyxy[0][1]), int(boxes.xyxy[0][2]), int(boxes.xyxy[0][3])))
    cv2.imwrite(os.path.join(output_path,filename), crop_image)
 
 