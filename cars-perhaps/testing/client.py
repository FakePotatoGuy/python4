import socket
import time

# !!! REPLACE WITH THE IP PRINTED BY THE SERVER SCRIPT !!!
SERVER_IP = "127.0.0.1" 
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((SERVER_IP, PORT))
    # Read the initial welcome message from server
    welcome_msg = client.recv(2048).decode('utf-8')
    print(welcome_msg)
except Exception as e:
    print(f"Could not connect to server: {e}")
    exit()

# Simple mock game loop (simulating player movement)
player_x, player_y = 0, 0

for i in range(10):
    player_x += 5  # Mock moving right
    player_y += 2  # Mock moving down
    
    try:
        # Send current local position to server
        position_string = f"{player_x},{player_y}"
        client.send(str.encode(position_string))
        
        # Receive overall network game state
        game_state = client.recv(2048).decode('utf-8')
        print(f"Server Game State: {game_state}")
        
    except Exception as e:
        print(f"Error transmitting data: {e}")
        break
        
    time.sleep(1) # Send update once per second

client.close()
