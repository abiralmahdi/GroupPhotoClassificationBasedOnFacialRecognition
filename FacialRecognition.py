import cv2
import face_recognition # pretrained model for facial features recognition

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Arrays which contain some random group images and some random user's images
arrUsers = ["abir.jpg","rdj.jpg", "rdj2.jpg", "biden.jpg"]
arrGroupImgs = ["group.webp", "rdj4.jpg", "rdj3.jpg","abirGroup.jpg"]

def recognition(imgArr, userImg):
    known_image = face_recognition.load_image_file(userImg) # Loading the image of the user
    known_encoding = face_recognition.face_encodings(known_image)[0] # Encoding of the user's image
    
    # This will loop over all the cropped faces in a group photo, and match the cropped faces with the 
    # user's image. If a match is found, it will return True, else False.
    for img in imgArr:
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert the image to RGB
        try:
            unknown_encoding = face_recognition.face_encodings(rgb_image)[0] # Find the encodings of the RGB image
        except Exception as e:
            pass

        # Use the compare_faces function of the facial_recognition model to compare the cropped face and the user's real face
        results = face_recognition.compare_faces([known_encoding], unknown_encoding) 
        
        if results[0]:
            return True
    return False


def cropOut(image_path, userImg):
    image = cv2.imread(image_path)
    imgArray = [] 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)      
    cv2.imshow('Image Window', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for i, (x, y, w, h) in enumerate(faces):
        face = image[y:y+h, x:x+w]
        imgArray.append(face)


