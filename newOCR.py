import cv2
import os
import time
import easyocr
import requests
import re
from secret import OPENAI_API_KEY

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def preprocess_text(text):
    # Remove non-alphanumeric characters and extra whitespace
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_shakespearean_poem(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-3.5-turbo-0613",
        "max_tokens": 200,
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "messages": [
            {"role": "system", "content": "You are a poetical assistant, skilled in composing verses with a Shakespearean flair."},
            {"role": "user", "content": "Can you generate a poem using these words:" + prompt}
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        poem = response_json["choices"][0]["message"]["content"]
        return preprocess_text(poem).strip()
    else:
        print("Error:", response.status_code)
        print("Response Content:", response.content)
        return "Error generating poem"

if __name__ == "__main__":
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam")
        exit()

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

                    # Generate and print a Shakespearean poem based on detected text
                    prompt = detection[1]
                    poem = generate_shakespearean_poem(prompt)
                    print(poem)

            # Wait for 10 seconds
            time.sleep(10)

            # Check for user input to break the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the capture
        cap.release()
        cv2.destroyAllWindows()
