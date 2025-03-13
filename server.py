import socket
import threading
import sys

def handle_client(client_socket, client_address, client_list):
    try:
        welcome_msg = f"Welcome! {len(client_list)} users online\n"
        client_socket.send(welcome_msg.encode("utf-8"))
        
        notify_msg = f"New user connected from {client_address[0]}:{client_address[1]}\n"
        broadcast(notify_msg, client_socket, client_list)
        
        while True:
            try:
                request = client_socket.recv(2048)
                if not request:  # Client disconnected
                    break
                    
                request = request.decode("utf-8")
                if request.strip() == "close":
                    break
                    
                sys.stdout.write(f"{client_address}> {request}")
                if not request.endswith('\n'):
                    sys.stdout.write('\n')
                sys.stdout.flush()
                
                broadcast(request, client_socket, client_list)
                
            except ConnectionError:
                break
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")
                break
    finally:
        print(f"Client {client_address} disconnected")
        client_socket.close()
        if client_socket in client_list:
            client_list.remove(client_socket)
        broadcast(f"User from {client_address[0]}:{client_address[1]} disconnected\n", None, client_list)

def broadcast(message, sender_socket, client_list):
    """Send message to all clients except the sender"""
    for client in client_list[:]:  # Create a copy to avoid modification during iteration
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                # Remove dead socket
                client.close()
                if client in client_list:
                    client_list.remove(client)

def run_server():
    client_list = []
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ("127.0.0.1", 8080)
        server.bind(server_address)
        
        server.listen(5)
        print(f"Server started on {server_address[0]}:{server_address[1]}")
        print("Waiting for connections...")
        
        while True:
            try:
                client_socket, client_address = server.accept()
                print(f"New connection from {client_address[0]}:{client_address[1]}")
                
                client_list.append(client_socket)
                
                thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_list))
                thread.daemon = True  # Allow the program to exit even if threads are running
                thread.start()
                
            except KeyboardInterrupt:
                print("\nShutting down server...")
                break
            except Exception as e:
                print(f"Error accepting connection: {e}")
    
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        for client in client_list:
            try:
                client.close()
            except:
                pass
        server.close()
        print("Server shutdown complete")

if __name__ == "__main__":
    run_server()
