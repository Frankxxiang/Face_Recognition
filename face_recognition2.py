import os
import cv2
import face_recognition
import sqlite3
import numpy as np

# Create a directory for storing face images
if not os.path.exists('faces'):
    os.makedirs('faces')

# Load the Haar Cascade algorithm from the XML file into OpenCV
alg = "haarcascade_frontalface_default.xml"
haar_cascade = cv2.CascadeClassifier(alg)

# Read the image in color
file_name = '00D0E3D9-9211-4138-AA99-700E6B83DC30_1_105_c.jpeg'
color_img = cv2.imread(file_name)

# Find the faces in the image
faces = haar_cascade.detectMultiScale(
    color_img,
    scaleFactor=1.05,
    minNeighbors=2,
    minSize=(100, 100)
)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('face_recognition.db')
cursor = conn.cursor()

# Create a table to store face encodings if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_name TEXT,
    face_encoding BLOB
)
''')

# For each face detected
i = 0
for x, y, w, h in faces:
    # Crop the image to select only the face
    cropped_image = color_img[y : y + h, x : x + w]
    
    # Save the cropped image
    target_file_name = 'faces/' + str(i) + '.jpg'
    cv2.imwrite(target_file_name, cropped_image)
    
    # Convert the cropped image to RGB (face_recognition uses RGB images)
    rgb_cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    
    # Get the face encodings
    face_encodings = face_recognition.face_encodings(rgb_cropped_image)
    
    if face_encodings:
        face_encoding = face_encodings[0]
        
        # Convert the face encoding to a binary format
        face_encoding_blob = np.array(face_encoding).tobytes()
        
        # Store the face encoding in the database
        cursor.execute('''
        INSERT INTO faces (person_name, face_encoding)
        VALUES (?, ?)
        ''', (f'Person_{i}', face_encoding_blob))
        
        print("Face encoding stored")
    
    i += 1

# Commit and close the database connection
conn.commit()
conn.close()

# Function to get face encodings from the database
def get_face_encodings_from_db():
    conn = sqlite3.connect('face_recognition.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT person_name, face_encoding FROM faces')
    rows = cursor.fetchall()
    
    known_face_encodings = []
    known_face_names = []
    
    for row in rows:
        person_name = row[0]
        face_encoding = np.frombuffer(row[1], dtype=np.float64)
        
        known_face_encodings.append(face_encoding)
        known_face_names.append(person_name)
    
    conn.close()
    
    return known_face_encodings, known_face_names

# Load a new image
new_image_file = '/Users/frank_xiang/PycharmProjects/game theory/dsadasdasds.jpeg'
new_image = cv2.imread(new_image_file)
rgb_new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)

# Get face encodings from the new image
new_face_encodings = face_recognition.face_encodings(rgb_new_image)

# Get known face encodings from the database
known_face_encodings, known_face_names = get_face_encodings_from_db()

for new_face_encoding in new_face_encodings:
    # Compare the new face encoding with known face encodings
    matches = face_recognition.compare_faces(known_face_encodings, new_face_encoding)
    
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
        print(f"Match found: {name}")
    else:
        print("No match found")
