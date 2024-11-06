import cv2
import face_recognition # pretrained model for facial features recognition
# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def recognize(users, groupImgs):
    for user in users:
        for groupImg in groupImgs:
            print(f"user: {user} \n froupimage {groupImg}")
            return cropOut(groupImg, user)

def recognition(image_path, imgArr, userImg):
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
            return image_path
    return False


def cropOut(image_path, userImg):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image at path {image_path}")
        return False  # or any appropriate return value to indicate failure

    imgArray = []  # Array to store the cropped images
    # Convert the image to grayscale as the face detector expects a gray image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Draw rectangles around each of the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Crop out the faces from the actual image
    for i, (x, y, w, h) in enumerate(faces):
        face = image[y:y + h, x:x + w]  # slice/crop the face
        imgArray.append(face)  # store the cropped image in an array

    return recognition(image_path, imgArray, userImg)



