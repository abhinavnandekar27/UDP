import socket

# Constants
UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 5005
BUFFER_SIZE = 1024

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))
print(f"Server listening on {UDP_IP}:{UDP_PORT}...")

# Function to process incoming messages
def process_message(packet):
    checksum, seq_num, message = packet.split(":", 2)
    # In a real-world scenario, you would recalculate the checksum to verify integrity
    # Here, we assume the message is valid and directly process it.
    print(f"Received message: {message} (Seq No: {seq_num})")
    return seq_num

# Main server loop
while True:
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Received data from {client_address}")
    
    # Decode the received data
    packet = data.decode()
    
    # Process and extract message
    seq_num = process_message(packet)
    
    # Send acknowledgment (ACK)
    ack_message = f"ACK for Seq No: {seq_num}"
    server_socket.sendto(ack_message.encode(), client_address)
    print(f"Sent ACK: {ack_message}")
