import cv2
import face_recognition # pretrained model for facial features recognition

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

arrUsers = ["abir.jpg","rdj.jpg", "rdj2.jpg", "biden.jpg"]
arrGroupImgs = ["group.webp", "rdj4.jpg", "rdj3.jpg","abirGroup.jpg"]

def test(users, groupImgs):
    for user in users:
        print("User-"+user)
        for groupImg in groupImgs:
            print(cropOut(groupImg, user))

def recognition(imgArr, userImg):
    known_image = face_recognition.load_image_file(userImg)
    known_encoding = face_recognition.face_encodings(known_image)[0]
    for img in imgArr:
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            unknown_encoding = face_recognition.face_encodings(rgb_image)[0]
        except Exception as e:
            pass
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        # print(str(results[0]) + str(count))
        if results[0]:
            return True
    return False
        
def cropOut(image_path, userImg):
    image = cv2.imread(image_path)
    imgArray = [] # Array to store the cropped faces
    # Convert the image to grayscale as the face detector expects a gray image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Only for testing, commented out by default. Uncomment this section if you want to test something ===============================        
    # Display the image in a window
    cv2.imshow('Image Window', image)
    # Wait for a key press indefinitely or for a specific amount of time (milliseconds)
    cv2.waitKey(0)
    # Close the window
    cv2.destroyAllWindows()
    # =====================================================================


    # Save the faces as a jpg image
    for i, (x, y, w, h) in enumerate(faces):
        # Crop the face from the original image
        face = image[y:y+h, x:x+w]
        # store the cropped face in the array
        imgArray.append(face)


    return recognition(imgArray, userImg)

print(test(arrUsers, arrGroupImgs))


