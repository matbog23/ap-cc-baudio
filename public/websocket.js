const socket = new WebSocket("ws://localhost:8765");
let isMusicPlaying = false; // Flag to track if music is already playing

socket.onopen = function (event) {
  console.log("WebSocket connection established.");
};

// Define music sequences for different moods
const sequences = {
  angry: ["C4", "D4", "F4", "G4", "A#4"],
  sad: ["E4", "G4", "A4", "A#4", "D5"],
  happy: ["C4", "E4", "G4", "C5", "E5"],
  neutral: ["C4", "D4", "E4", "F4", "G4"],
};

// Function to play music based on mood
function playMusic(mood) {
  const notes = sequences[mood];
  const synth = new Tone.Synth().toDestination();
  const sequence = new Tone.Sequence(
    (time, note) => {
      synth.triggerAttackRelease(note, "8n", time);
    },
    notes,
    "8n"
  );

  // Start the music only if it's not already playing
  if (!isMusicPlaying) {
    Tone.Transport.start();
    sequence.start();
    isMusicPlaying = true;
  } else {
    // Update the sequence if music is already playing
    sequence.start();
  }
}

// Add event listener to start playback button
const startPlaybackButton = document.getElementById("startPlaybackButton");
startPlaybackButton.addEventListener("click", async function () {
  // Send request to server to get sentiment
  // For demonstration purposes, let's assume sentiment is "happy"
  const sentiment = "happy";
  console.log("Sentiment requested:", sentiment);

  // Await the playMusic function
  await playMusic(sentiment);

  // This code will only execute after playMusic has finished
  console.log("Music playback complete.");
});

// Handle WebSocket message
socket.onmessage = async function (event) {
  const sentiment = event.data;
  console.log("Received sentiment from server:", sentiment);

  // Play music based on sentiment
  await playMusic(sentiment);

  // This code will only execute after playMusic has finished
  console.log("Music playback complete.");
};
