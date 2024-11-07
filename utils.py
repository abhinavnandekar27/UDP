import hashlib

# Function to calculate checksum using SHA256 (for simplicity)
def calculate_checksum(data: str) -> str:
    checksum = hashlib.sha256(data.encode()).hexdigest()
    return checksum
