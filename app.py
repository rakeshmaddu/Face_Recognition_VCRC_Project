from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import sqlite3
from datetime import datetime
import face_recognition

app = Flask(__name__)

# Load known face encodings
known_faces = {
    "Koppuravuri Venkata Naga Sai Mahendra": {
        "encoding": face_recognition.face_encodings(face_recognition.load_image_file("person1.jpg"))[0],
        "department": "NWC",
        "registration_number": "RA2211028010158"
    },
    "Maddu Rakesh": {
        "encoding": face_recognition.face_encodings(face_recognition.load_image_file("person2.jpg"))[0],
        "department": "NWC",
        "registration_number": "RA2211028010159"
    },
     "Konijeti Sai Kalyan": {
        "encoding": face_recognition.face_encodings(face_recognition.load_image_file("person3.jpg"))[0],
        "department": "NWC",
        "registration_number": "RA2211028010160"
    }
    # Add more known persons here as needed
}

# Initialize the database
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            registration_number TEXT,
            login_time TEXT,
            logout_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def recognize_faces(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    return face_encodings

def is_match(known_encoding, test_encoding, threshold=0.6):
    return face_recognition.compare_faces([known_encoding], test_encoding, tolerance=threshold)[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    encodings = recognize_faces(image)
    if len(encodings) > 0:
        test_encoding = encodings[0]
        found = False
        
        # Iterate through known faces to match the test encoding
        for name, details in known_faces.items():
            known_encoding = details['encoding']
            if is_match(known_encoding, test_encoding):
                found = True
                login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                conn = sqlite3.connect('attendance.db')
                c = conn.cursor()

                # Check if user has already logged in and hasn't logged out
                c.execute('''
                    SELECT * FROM attendance WHERE name=? AND logout_time IS NULL
                ''', (name,))
                record = c.fetchone()

                if record:
                    # Update the logout time for existing record
                    c.execute('''
                        UPDATE attendance SET logout_time=? WHERE id=?
                    ''', (login_time, record[0]))
                else:
                    # Insert a new login record
                    c.execute('''
                        INSERT INTO attendance (name, department, registration_number, login_time, logout_time)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, details['department'], details['registration_number'], login_time, None))

                conn.commit()
                conn.close()

                return jsonify({"result": f"Face recognized as {name}. Attendance recorded."})

        # If no match found
        if not found:
            return jsonify({"result": "Face not recognized. No record added."})
    else:
        return jsonify({"result": "No faces detected in the image."})

@app.route('/logout', methods=['POST'])
def logout():
    try:
        registration_number = request.form.get('registration_number')
        logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()

        # Update logout time for the given registration number
        c.execute('''
            UPDATE attendance
            SET logout_time = ?
            WHERE registration_number = ? AND logout_time IS NULL
        ''', (logout_time, registration_number))

        conn.commit()
        conn.close()

        return jsonify({"result": "Logout time recorded."})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"result": "Error occurred while recording logout time."})

if __name__ == '__main__':
    app.run(debug=True)
