import socket
import threading

# Automatically get the host's LAN IP address
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))
server.listen()

print(f"[START] Server is listening on {SERVER_IP}:{PORT}")

# Game state: Dictionary storing positions of connected players
# Format: { client_id: "x,y" }
players = {}

def handle_client(conn, player_id):
    """Handles communication with a single connected player."""
    print(f"[NEW CONNECTION] Player {player_id} connected.")
    
    # Send initial setup package to the client
    conn.send(str.encode(f"Welcome Player {player_id}"))
    
    while True:
        try:
            # Receive data from client (e.g., "100,250")
            data = conn.recv(2048).decode('utf-8')
            if not data:
                break
                
            players[player_id] = data
            
            # Send back the full state of all players to this client
            # Format sent back: "id1:x,y|id2:x,y"
            reply = "|".join([f"{k}:{v}" for k, v in players.items()])
            conn.sendall(str.encode(reply))
            
        except Exception as e:
            print(f"[ERROR] Player {player_id} disconnected: {e}")
            break

    # Clean up on disconnect
    if player_id in players:
        del players[player_id]
    conn.close()

player_count = 0
while True:
    conn, addr = server.accept()
    player_count += 1
    # Start a new thread for every client that joins
    thread = threading.Thread(target=handle_client, args=(conn, player_count))
    thread.start()
