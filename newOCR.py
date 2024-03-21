import cv2
import os
import time
import easyocr

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        # Display the captured frame
        cv2.imshow('Webcam', frame)

        # Save the image with a unique filename (timestamp)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"captured_image_{timestamp}.jpg"
        cv2.imwrite(filename, frame)

        # Read text from the captured image
        result = reader.readtext(filename)

        # Print the detected text
        if result:
            print("Detected Text:")
            for detection in result:
                print(detection[1])

        #stuur de data van 'detection' in een bericht naar openAI API en vraag voor het gevoel te kiezen uit een lijst van opties.
                
        #Stuur dat antwoord via een websocket naar de index.html file zodat tone.js daar een geluid kan afspelen.

        # Wait for 10 seconds
        time.sleep(10)

        # Check for user input to break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the capture
    cap.release()
    cv2.destroyAllWindows()
