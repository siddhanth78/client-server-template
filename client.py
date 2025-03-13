import socket
import sys
import select

def run_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("127.0.0.1", 8080)
        client.connect(server_address)
        print(f"Connected to server at {server_address[0]}:{server_address[1]}")
        
        while True:
            sockets_list = [sys.stdin, client]
            read_sockets, _, error_sockets = select.select(sockets_list, [], sockets_list)
            
            for sock in read_sockets:
                if sock == client:
                    try:
                        response = client.recv(2048)
                        if not response:
                            print("Server disconnected")
                            return
                        response = response.decode("utf-8")
                        sys.stdout.write(f"> {response}")
                        if not response.endswith('\n'):
                            sys.stdout.write('\n')
                        sys.stdout.flush()
                    except:
                        print("Connection lost")
                        return
                else:
                    message = sys.stdin.readline()
                    client.send(message.encode("utf-8"))
                    sys.stdout.flush()
                    if message.strip() == "close":
                        print("Disconnecting from server...")
                        client.close()
                        return
            
            for sock in error_sockets:
                print("Error occurred, disconnecting")
                sock.close()
                return
                
    except ConnectionRefusedError:
        print("Could not connect to server. Is it running?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            client.close()
        except:
            pass

if __name__ == "__main__":
    run_client()
