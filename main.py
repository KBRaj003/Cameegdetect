
import cv2
import numpy as np
import time

def main():
    # Initialize the webcam (0 is usually the built-in front camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Initialize face and eye detectors using OpenCV's built-in Haar Cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    print("Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Region of Interest (ROI) for the face
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # Detect eyes within the face ROI
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            for (ex, ey, ew, eh) in eyes:
                # Draw a rectangle around the eye
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                
                # Isolate the eye region for pupil detection
                eye_roi = roi_gray[ey:ey+eh, ex:ex+ew]
                
                # Apply a binary threshold to isolate the dark pupil
                _, thresh = cv2.threshold(eye_roi, 60, 255, cv2.THRESH_BINARY_INV)
                
                # Find contours in the thresholded image
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if contours:
                    # Find the largest contour (likely the pupil)
                    largest_contour = max(contours, key=cv2.contourArea)
                    if cv2.contourArea(largest_contour) > 10:
                        # Calculate the bounding circle for the pupil
                        (cx, cy), radius = cv2.minEnclosingCircle(largest_contour)
                        center = (int(cx), int(cy))
                        
                        # Draw the circle on the main frame
                        cv2.circle(roi_color, (int(ex + cx), int(ey + cy)), int(radius), (0, 0, 255), 2)
                        
                        # Display pupil radius on screen as a proxy for cognitive state
                        cv2.putText(frame, f"Pupil Radius: {radius:.1f}px", (x, y-10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Pupillometry via OpenCV', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
