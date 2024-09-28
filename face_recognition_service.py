import cv2
import numpy as np
import face_recognition

# Load known faces and encodings
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
}

# Recognize faces function
def recognize_faces(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    return face_encodings

# Function to compare faces
def is_match(known_encoding, test_encoding, threshold=0.6):  # Adjusted threshold
    return face_recognition.compare_faces([known_encoding], test_encoding, tolerance=threshold)[0]

# Main function
def main():
    # Initialize the video capture from camera
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to capture image.")
            break

        # Get face encodings from the captured frame
        encodings = recognize_faces(frame)

        if len(encodings) > 0:
            test_encoding = encodings[0]
            found = False

            # Iterate through known faces to find a match
            for name, details in known_faces.items():
                known_encoding = details['encoding']

                if is_match(known_encoding, test_encoding):
                    found = True
                    print(f"Face recognized as {name}")
                    print(f"Details: Department: {details['department']}, Registration Number: {details['registration_number']}")
                    break

            if not found:
                print("Face not recognized.")
        else:
            print("No faces detected.")

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
