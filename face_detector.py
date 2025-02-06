from deepface import DeepFace
import matplotlib.pyplot as plt
# from Image_proccess import *
import cv2
import os

image_path="ImageRaw"
image_size=216
imageraw_path="ID_image"

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
  'fastmtcnn',
]

imgList=[]
for filename in os.listdir(imageraw_path):
    imgList.append(filename)
    print(imgList)

for image_name in imgList:
  image=cv2.imread(os.path.join(imageraw_path,image_name))
  # print(image)
  height, width,_=image.shape
  image=cv2.resize(image,(int(width/2),int(height/2)))

  face_objs = DeepFace.extract_faces(img_path = image, 
          detector_backend = backends[3]
  )
  # plt.imshow(face_objs)
  # print(test2.jpg)
  # img_list=['test2.jpg']

  # cv2.imshow("ID Img", image)


  # print(height, width)

  face_objs=face_objs[0]

  max_length=max(image_size,face_objs["facial_area"]["w"],face_objs["facial_area"]["h"])
  min_length=min(image_size,face_objs["facial_area"]["w"],face_objs["facial_area"]["h"])
  min_length=int(min_length/4)

  y_coordinates_face=face_objs["facial_area"]["y"]
  x_coordinates_face=face_objs["facial_area"]["x"]

  crop_image = image[y_coordinates_face-min_length:y_coordinates_face-min_length+max_length,x_coordinates_face-min_length:x_coordinates_face-min_length+max_length]
  crop_image=cv2.resize(crop_image,(image_size,image_size))

  cv2.imshow("crop Img", crop_image)
  cv2.waitKey(0)
  cv2.imwrite(os.path.join(image_path,image_name), crop_image) 
  # print(face_objs["facial_area"])
  print(image_name)