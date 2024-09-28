# Face_Recognition_VCRC_Project
Face Recognition Attendance System
Overview
The Face Recognition Attendance System is a web-based application that automates attendance tracking through facial recognition technology. Designed for educational institutions and workplaces, this system captures real-time video feeds from a camera, detects faces, and matches them against a database of known individuals. Upon identification, the system logs the attendance of the individual in an SQLite database, streamlining the attendance management process.

Features
Real-Time Face Recognition: The application can detect and recognize faces using webcam input, ensuring instant attendance recording.
Automated Attendance Logging: Attendance records, including login and logout times, are automatically maintained in an SQLite database, reducing administrative workload.
User-Friendly Interface: A simple web interface enables easy interaction for users of all technical levels.
Data Storage: The system stores known faces and attendance records, ensuring data consistency and retrievability.
Bounding Box Visualization: Each recognized face is highlighted with a bounding box for better visual feedback, enhancing user experience.
Technologies Used
Backend: Flask (Python)
Face Recognition: Face_recognition library
Database: SQLite
Frontend: HTML, CSS, JavaScript
Video Processing: OpenCV
