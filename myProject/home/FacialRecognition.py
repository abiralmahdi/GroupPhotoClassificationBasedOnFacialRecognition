import cv2
import face_recognition # pretrained model for facial features recognition
# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Arrays which contain some random group images and some random user's images
arrUsers = ["abir.jpg","rdj.jpg", "rdj2.jpg", "biden.jpg"]
arrGroupImgs = ["group.webp", "rdj4.jpg", "rdj3.jpg","abirGroup.jpg"]


def recognition(img, userImg):
    # Load the user's image and compute its encoding
    known_image = face_recognition.load_image_file(userImg)
    known_encodings = face_recognition.face_encodings(known_image)
    if not known_encodings:
        # Handle case where no face is detected in the user's image
        print("No face detected in the user's image.")
        return False
    known_encoding = known_encodings[0]
    # Load and process the input image
    image = cv2.imread(img)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    try:
        # Attempt to compute the encoding for the face in the image
        unknown_encodings = face_recognition.face_encodings(rgb_image)
        
        if not unknown_encodings:
            # No face detected in the input image
            return False
        
        # Use the first encoding if multiple faces are detected
        unknown_encoding = unknown_encodings[0]
    except Exception as e:
        # Log or handle the exception (optional)
        print(f"Error during face encoding: {e}")
        return False  # Fail gracefully if encoding fails
    
    # Compare the faces and return the result
    results = face_recognition.compare_faces([known_encoding], unknown_encoding)
    return results[0]


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

    return recognition(imgArray, userImg)
