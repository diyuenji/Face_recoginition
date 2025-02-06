# This project create a real time app for facial recognition 

## How to use
1.1 If you already have your facial image, put it in ImageRaw Folder then run Image_process.py or face_detector.py for reprocess your raw image to image that fit requirements//
1.2 If you dont have your facial image, you can put your ID_card image in ID_image then run crop_personal_img.py which will crop your facial image in ID card and put it in ImageRaw Folder//
2. Push manual some information from ID card to Firebase server through AddDataToDatabase.py//
3. Run EnccodeGenerator.py to create pickle file which learn from all user's facial image and use it for main.py//
4. Run main.py//

## Futher work
- Create a OCR model for auto exactly extract information from user's ID card to json type then push to Firebase server//
- Create a code to reprocess ID card (crop fit ID card, rotate,....) which help model OCR work better. 
