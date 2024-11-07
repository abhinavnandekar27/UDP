// script.js

// Elements from the UI
const startButton = document.getElementById('startTransmission');
const statusElement = document.getElementById('transmissionStatus');
const logList = document.getElementById('logList');

// Simulating packet transmission (instead of actual UDP socket for the web)
let packetSeqNo = 1;
let maxRetries = 3;
let retries = 0;
let transmissionInProgress = false;

// Function to simulate sending a packet and logging the status
function sendPacket(seqNo) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simulate 90% success rate for sending a packet
            const success = Math.random() > 0.1; // 10% chance of failure
            if (success) {
                logStatus(`Sent packet ${seqNo} (Success)`);
                resolve(seqNo);
            } else {
                logStatus(`Sent packet ${seqNo} (Failure)`);
                reject(seqNo);
            }
        }, 1000);
    });
}

// Function to log statuses in the UI
function logStatus(message) {
    const listItem = document.createElement('li');
    listItem.textContent = message;
    logList.appendChild(listItem);
}

// Function to handle the retransmission logic
async function handleTransmission() {
    transmissionInProgress = true;
    statusElement.textContent = "Transmitting...";

    // Simulate sending a number of packets
    for (let i = 1; i <= 10; i++) {
        let attempts = 0;
        while (attempts < maxRetries) {
            try {
                await sendPacket(i); // Attempt to send packet
                break; // If successful, move to the next packet
            } catch (error) {
                attempts++;
                logStatus(`Timeout! Retrying packet ${i} (${attempts}/${maxRetries})`);
                if (attempts === maxRetries) {
                    logStatus(`Failed to send packet ${i} after ${maxRetries} attempts.`);
                }
            }
        }
    }

    transmissionInProgress = false;
    statusElement.textContent = "Transmission Complete";
}

// Event listener to start the transmission when the button is clicked
startButton.addEventListener('click', () => {
    if (!transmissionInProgress) {
        logStatus("Starting transmission...");
        handleTransmission();
    }
});
