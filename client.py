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

def roomlist(client_socket, mode):
    message = f"ROOMLIST:{mode}"
    client_socket.send(message.encode())
    
    response = client_socket.recv(1024).decode()
    
    if response == "REGISTER:ACKSTATUS:1":
        print("Error: Please input a valid mode.")

    print(response)

def main_menu():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))
    
    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. Register")
        print("3. Roomlist")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(client_socket, username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(client_socket, username, password)
        elif choice == '3':
            mode = input("Enter mode (PLAYER/VIEWER): ")
            roomlist(client_socket, mode)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
