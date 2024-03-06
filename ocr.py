import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture(0)  # Use 0 for default camera

# Instance text detector
reader = easyocr.Reader(['en, nl'], gpu=True)

# Define threshold
threshold = 0.25

# Create a log file to store text data
log_file_path = 'text_log.txt'
with open(log_file_path, 'w') as log_file:
    # Write header to log file
    log_file.write("Text Log\n")
    log_file.write("Text | Bounding Box (x1, y1, x2, y2) | Confidence Score\n")
    
    while True:
        # Read frame from the camera
        ret, frame = cap.read()

        # Check if frame is read successfully
        if not ret:
            break

        # Display the frame (optional)
        cv2.imshow('Live Video', frame)

        # Perform OCR on the frame with easyOCR
        # Detect text on frame
        text_ = reader.readtext(frame)

        # Draw bounding boxes and text
        for bbox, text, score in text_:
            if score > threshold:
                # Extract coordinates of the bounding box
                x1, y1 = bbox[0]
                x2, y2 = bbox[2]
                # Convert coordinates to integers
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # Draw rectangle
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                # Add text
                cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
                
                # Write data to log file
                log_file.write(f"{text} | ({x1}, {y1}, {x2}, {y2}) | {score}\n")

        # Display the annotated frame
        cv2.imshow('Annotated Video', frame)
                
        # Save the annotated frame to a specific path
        #annotated_image_path = 'annotated_image.jpg'
        #cv2.imwrite(annotated_image_path, frame)
        #print("Annotated image saved at:", annotated_image_path)


        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Print path to log file
print("Text log saved at:", log_file_path)

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
