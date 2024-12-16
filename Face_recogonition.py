import os
if not os.path.exists('faces'):
    os.makedirs('faces')

import cv2

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

# For each face detected
i = 0
for x, y, w, h in faces:
    # Crop the image to select only the face
    cropped_image = color_img[y : y + h, x : x + w]
    
    # Write the cropped image to a file
    target_file_name = 'faces/' + str(i) + '.jpg'
    cv2.imwrite(target_file_name, cropped_image)
    print("yes")
    i += 1
