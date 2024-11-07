import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))
print(f"Server listening on {UDP_IP}:{UDP_PORT}...")

def process_message(packet):
    checksum, seq_num, message = packet.split(":", 2)
    print(f"Received message: {message} (Seq No: {seq_num})")
    return seq_num

while True:
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Received data from {client_address}")
    
    packet = data.decode()
    
    seq_num = process_message(packet)
    
    ack_message = f"ACK for Seq No: {seq_num}"
    server_socket.sendto(ack_message.encode(), client_address)
    print(f"Sent ACK: {ack_message}")
