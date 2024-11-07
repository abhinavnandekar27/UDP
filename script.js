const startButton = document.getElementById('startTransmission');
const statusElement = document.getElementById('transmissionStatus');
const logList = document.getElementById('logList');

let packetSeqNo = 1;
let maxRetries = 3;
let retries = 0;
let transmissionInProgress = false;

function sendPacket(seqNo) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const success = Math.random() > 0.1;
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

function logStatus(message) {
    const listItem = document.createElement('li');
    listItem.textContent = message;
    logList.appendChild(listItem);
}

async function handleTransmission() {
    transmissionInProgress = true;
    statusElement.textContent = "Transmitting...";

    for (let i = 1; i <= 10; i++) {
        let attempts = 0;
        while (attempts < maxRetries) {
            try {
                await sendPacket(i);
                break;
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

startButton.addEventListener('click', () => {
    if (!transmissionInProgress) {
        logStatus("Starting transmission...");
        handleTransmission();
    }
});
