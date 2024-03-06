// script.js

function updateOCRText() {
  // Fetch the text from the server
  fetch("text_log.txt")
    .then((response) => response.text())
    .then((text) => {
      // Display the text in the paragraph
      document.getElementById("ocr-text").textContent = text;

      // Schedule the next update after a short delay
      setTimeout(updateOCRText, 1000); // Update every 1 second (adjust as needed)
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Call the function to start updating the OCR text
updateOCRText();
