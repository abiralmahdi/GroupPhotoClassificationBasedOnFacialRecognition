import cv2
import face_recognition
import pyttsx3

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Arrays which contain some random group images and their labels
arrGroupImgs = [
    ("images/group.webp", "Group 1"), 
    ("images/rdj4.jpg", "RDJ 4"), 
    ("images/rdj3.jpg", "RDJ 3"), 
    ("images/abirGroup.jpg", "Abir Group"),
    ("images/sam1.jpg", "Samia 1"),
    ("images/sam2.jpg", "samia 2"),
    ("images/Anmol.jpg", "Anmol")
]

def recognition(cropped_face, user_encoding):
    try:
        face_encoding = face_recognition.face_encodings(cropped_face)[0]  # Encode the cropped face
        return face_recognition.compare_faces([user_encoding], face_encoding)[0]  # Check for a match
    except IndexError:
        # Return False if encoding fails (no face found or other issue)
        return False

def crop_faces(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image at path {image_path}")
        return []

    cropped_faces = []  # Array to store the cropped face regions
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face = image[y:y + h, x:x + w]
        cropped_faces.append(face)

    return cropped_faces

# Pre-process group images: encode and store each face in each group image
group_faces_encodings = []
for image_path, label in arrGroupImgs:
    cropped_faces = crop_faces(image_path)
    for face in cropped_faces:
        rgb_face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        try:
            encoding = face_recognition.face_encodings(rgb_face)[0]
            group_faces_encodings.append((encoding, label))
        except IndexError:
            # Skip if encoding fails
            continue

# Open the webcam and process frames
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture image from webcam.")
        break

    # Convert the frame to RGB for face recognition processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        match_found = False
        label = "Unknown"

        # Compare the webcam face with each pre-encoded face in group images
        for group_encoding, group_label in group_faces_encodings:
            match = face_recognition.compare_faces([group_encoding], face_encoding)
            if match[0]:
                label = group_label
                match_found = True
                break

        # Draw bounding box and label
        color = (0, 255, 0) if match_found else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, label, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Output label through audio
        engine.say(label)
        engine.runAndWait()

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
