import cv2
import face_recognition # pretrained model for facial features recognition

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def recognition(imgArr, userImg):
    known_image = face_recognition.load_image_file(userImg) # Loading the image of the user
    known_encoding = face_recognition.face_encodings(known_image)[0] # Encoding of the user's image
    
    # This will loop over all the cropped faces in a group photo, and match the cropped faces with the 
    # user's image. If a match is found, it will return True, else False.
    for img in imgArr:
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        try:
            unknown_encoding = face_recognition.face_encodings(rgb_image)[0]
        except Exception as e:
            pass
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        if results[0]:
            return True
    return False



