import socket

def login(client_socket, username, password):
    message = f"LOGIN:{username}:{password}"
    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()
    if response == "LOGIN:ACKSTATUS:0":
        print(f"Welcome {username}")
    elif response == "LOGIN:ACKSTATUS:1":
        print(f"Error: User {username} not found")
    elif response == "LOGIN:ACKSTATUS:2":
        print(f"Error: Wrong password for user {username}")
    elif response == "LOGIN:ACKSTATUS:3":
        print("Error: Invalid LOGIN message format")

def register(client_socket, username, password):
    message = f"REGISTER:{username}:{password}"
    client_socket.send(message.encode())
    
    response = client_socket.recv(1024).decode()
    
    if response == "REGISTER:ACKSTATUS:0":
        print(f"Successfully created user account {username}")
    elif response == "REGISTER:ACKSTATUS:1":
        print(f"Error: User {username} already exists")
    elif response == "REGISTER:ACKSTATUS:2":
        print("Error: Invalid REGISTER message format")

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))
    
    # Lựa chọn thao tác đăng nhập hoặc đăng ký
    action = input("Do you want to [login] or [register]? ").strip().lower()
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if action == "login":
        login(client_socket, username, password)
    elif action == "register":
        register(client_socket, username, password)
    else:
        print("Invalid action.")
    
    client_socket.close()

if __name__ == "__main__":
    
    start_client()
