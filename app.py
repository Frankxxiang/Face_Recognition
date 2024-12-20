from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import sqlite3
import numpy as np
import cv2
import os
from flask import send_from_directory


# 创建 Flask 应用实例
app = Flask(__name__)

# 允许跨域请求
CORS(app)

# 连接到 SQLite 数据库
conn = sqlite3.connect('face_recognition.db', check_same_thread=False)
cursor = conn.cursor()

# 如果表不存在则创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_name TEXT,
    face_encoding BLOB
)
''')
print("database initialized!")

# 定义上传图片的路由
@app.route('/upload', methods=['POST'])
def upload_image():
    print("line 34,app.py")
    # 获取上传的文件
    file = request.files['image']
    # 使用 face_recognition 加载图片
    image = face_recognition.load_image_file(file)
    # 获取图片中的面部编码
    face_encodings = face_recognition.face_encodings(image)

    # 如果没有找到面部编码，返回错误信息
    if not face_encodings:
        print("No Faces Found!")
        return jsonify({"error": "No faces found"}), 400

    # 取第一个面部编码
    face_encoding = face_encodings[0]
    # 将面部编码转换为二进制数据
    face_encoding_blob = np.array(face_encoding).tobytes()

    # 将面部编码保存到数据库
    cursor.execute('''
    INSERT INTO faces (person_name, face_encoding)
    VALUES (?, ?)
    ''', ('Unknown', face_encoding_blob))
    conn.commit()
    print("Faces stored!")

    # 截取面部图像并保存为文件
    face_locations = face_recognition.face_locations(image)
    top, right, bottom, left = face_locations[0]
    face_image = image[top:bottom, left:right]
    face_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)  # 转换为BGR格式以便OpenCV处理
    face_filename = f"static/faces/face_{cursor.lastrowid}.jpg"
    cv2.imwrite(face_filename, face_image)

    # 返回成功信息
    return jsonify({"message": "Face encoding stored", "image_url": face_filename}), 200

# 定义获取所有面部信息的路由
@app.route('/faces', methods=['GET'])
def get_faces():
    # 查询数据库中的所有面部信息
    cursor.execute('SELECT id, person_name FROM faces')
    faces = cursor.fetchall()
    # 返回查询结果
    return jsonify(faces), 200

# 定义比较面部信息的路由
@app.route('/compare', methods=['POST'])
def compare_faces():
    # 获取上传的文件
    file = request.files['image']
    # 使用 face_recognition 加载图片
    image = face_recognition.load_image_file(file)
    # 获取图片中的面部编码
    face_encodings = face_recognition.face_encodings(image)

    # 如果没有找到面部编码，返回错误信息
    if not face_encodings:
        print("No faces found in Compare Faces process!")
        return jsonify({"error": "No faces found"}), 400

    # 取第一个面部编码
    new_face_encoding = face_encodings[0]

    # 从数据库中获取已知的面部编码
    cursor.execute('SELECT id, person_name, face_encoding FROM faces')
    rows = cursor.fetchall()

    # 将数据库中的二进制面部编码转换为 numpy 数组
    known_face_encodings = [np.frombuffer(row[2], dtype=np.float64) for row in rows]
    known_face_names = [row[1] for row in rows]

    # 比较上传的面部编码和数据库中的面部编码
    matches = face_recognition.compare_faces(known_face_encodings, new_face_encoding)
    results = []

    # 如果找到匹配的面部编码，添加到结果列表中
    for i, match in enumerate(matches):
        if match:
            results.append(known_face_names[i])

    # 返回匹配结果
    if results:
        return jsonify({"matches": results}), 200
    else:
        return jsonify({"matches": []}), 200

@app.route('/faces/<filename>')
def get_face_image(filename):
    return send_from_directory('static/faces', filename)


# 启动 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
