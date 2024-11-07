import socket
import time
import random
from utils import calculate_checksum

# Constants
UDP_IP = "127.0.0.1"  # Server's IP (update with Windows PC IP if different)
UDP_PORT = 5005
BUFFER_SIZE = 1024
TIMEOUT = 2  # Timeout in seconds for waiting ACK
MAX_RETRIES = 3  # Max number of retransmissions for missing datagrams
WINDOW_SIZE = 5  # Flow control - Max number of unacknowledged packets

# Track acknowledged packets
acknowledged_packets = set()

# Function to send a message with sequence number and checksum
def send_message(message: str, seq_num: int, retries: int = 0):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    checksum = calculate_checksum(message)
    packet = f"{checksum}:{seq_num}:{message}"

    # Send the packet
    client_socket.sendto(packet.encode(), (UDP_IP, UDP_PORT))
    print(f"Sent message: {message} (Seq No: {seq_num})")

    # Set timeout for ACK
    client_socket.settimeout(TIMEOUT)

    try:
        ack, _ = client_socket.recvfrom(BUFFER_SIZE)
        print("Received ACK:", ack.decode())
        acknowledged_packets.add(seq_num)
    except socket.timeout:
        if retries < MAX_RETRIES:
            print(f"Timeout! No ACK received for Seq No: {seq_num}. Retrying... ({retries + 1}/{MAX_RETRIES})")
            send_message(message, seq_num, retries + 1)  # Resend the packet if no ACK received
        else:
            print(f"Failed to receive ACK for Seq No: {seq_num}. Giving up after {MAX_RETRIES} retries.")

    client_socket.close()

# Function to control flow with sliding window
def send_with_flow_control():
    for seq_num in range(1, 21):  # Send 20 messages
        if len(acknowledged_packets) >= WINDOW_SIZE:
            print(f"Window full. Waiting for ACKs before sending more messages.")
            time.sleep(2)  # Simulate waiting for ACKs

        message = f"Hello, this is packet {seq_num}"
        send_message(message, seq_num)
        time.sleep(0.5)  # Simulate delay between packet sends

# Start the client and send messages
def start_client():
    send_with_flow_control()

if __name__ == "__main__":
    start_client()