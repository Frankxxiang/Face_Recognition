from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import sqlite3
import numpy as np
import cv2
import os

app = Flask(__name__)
CORS(app)

# Connect to SQLite database
conn = sqlite3.connect('face_recognition.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_name TEXT,
    face_encoding BLOB
)
''')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    image = face_recognition.load_image_file(file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return jsonify({"error": "No faces found"}), 400

    face_encoding = face_encodings[0]
    face_encoding_blob = np.array(face_encoding).tobytes()

    # Save face encoding to database
    cursor.execute('''
    INSERT INTO faces (person_name, face_encoding)
    VALUES (?, ?)
    ''', ('Unknown', face_encoding_blob))
    conn.commit()

    return jsonify({"message": "Face encoding stored"}), 200

@app.route('/faces', methods=['GET'])
def get_faces():
    cursor.execute('SELECT id, person_name FROM faces')
    faces = cursor.fetchall()
    return jsonify(faces), 200

@app.route('/compare', methods=['POST'])
def compare_faces():
    file = request.files['image']
    image = face_recognition.load_image_file(file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return jsonify({"error": "No faces found"}), 400

    new_face_encoding = face_encodings[0]

    # Get known face encodings from database
    cursor.execute('SELECT id, person_name, face_encoding FROM faces')
    rows = cursor.fetchall()

    known_face_encodings = [np.frombuffer(row[2], dtype=np.float64) for row in rows]
    known_face_names = [row[1] for row in rows]

    matches = face_recognition.compare_faces(known_face_encodings, new_face_encoding)
    results = []

    for i, match in enumerate(matches):
        if match:
            results.append(known_face_names[i])

    if results:
        return jsonify({"matches": results}), 200
    else:
        return jsonify({"matches": []}), 200

if __name__ == '__main__':
    app.run(debug=True)
