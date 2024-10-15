import socket
import bcrypt
import json
import os

# Tên tệp JSON để lưu cơ sở dữ liệu
USER_DB_FILE = 'user_db.json'

# Khởi tạo danh sách phòng
available_rooms = [
    "Room 1",
    "epic room 2",
    "another epic room"
]

# Đọc cơ sở dữ liệu người dùng từ tệp JSON
def load_user_database():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            user_db = json.load(f)
            # Chuyển đổi mật khẩu lưu từ chuỗi JSON sang bytes cho bcrypt
            return {username: password.encode('utf-8') for username, password in user_db.items()}
    return {}

# Lưu cơ sở dữ liệu người dùng vào tệp JSON
def save_user_database():
    with open(USER_DB_FILE, 'w') as f:
        json.dump({username: hashed_password.decode('utf-8') for username, hashed_password in user_db.items()}, f)
    print("User database updated.")

# Khởi tạo cơ sở dữ liệu từ tệp JSON
user_db = load_user_database()

# Hàm gửi thông báo BADAUTH
def send_badauth(client_socket):
    client_socket.send("BADAUTH".encode())
    print("Error: You must be logged in to perform this action.")

# Hàm đăng nhập người dùng
def login_user(client_socket, username, password):
    if username in user_db:
        if bcrypt.checkpw(password.encode(), user_db[username]):
            client_socket.send("LOGIN:ACKSTATUS:0".encode())
            print(f"{username} has successfully logged in.")
            return True  # Trả về True nếu đăng nhập thành công
    else:
        client_socket.send("LOGIN:ACKSTATUS:1".encode())
        print(f"User {username} not found.")

    client_socket.send("LOGIN:ACKSTATUS:2".encode())
    print(f"Wrong password attempt for {username}.")
    return False  # Trả về False nếu không đăng nhập thành công

# Hàm đăng ký người dùng
def register_user(client_socket, username, password):
    if username in user_db:
        client_socket.send("REGISTER:ACKSTATUS:1".encode())
        print(f"User {username} already exists.")
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user_db[username] = hashed_password
        save_user_database()
        
        client_socket.send("REGISTER:ACKSTATUS:0".encode())
        print(f"User {username} successfully registered.")

# Hàm xử lý yêu cầu ROOMLIST
def room_list(client_socket, mode):
    if mode not in ["PLAYER", "VIEWER"]:
        client_socket.send("ROOMLIST:ACKSTATUS:1".encode())
        print("Error: Please input a valid mode.")
        return
    
    room_list_string = ",".join(available_rooms)
    response = f"ROOMLIST:ACKSTATUS:0:{room_list_string}"
    client_socket.send(response.encode())
    print(f"Sent room list to client: {response}")

# Hàm xử lý yêu cầu từ client
def handle_client(client_socket):
    logged_in_users = set()  # Giữ trạng thái người dùng đã đăng nhập
    
    while True:
        message = client_socket.recv(1024).decode()
        
        if message.startswith("LOGIN:"):
            parts = message.split(":")
            
            if len(parts) != 3:
                client_socket.send("LOGIN:ACKSTATUS:3".encode())
                continue
            
            username = parts[1]
            password = parts[2]
            if login_user(client_socket, username, password):
                logged_in_users.add(username)  # Đánh dấu người dùng là đã đăng nhập

        elif message.startswith("REGISTER:"):
            parts = message.split(":")
            
            if len(parts) != 3:
                client_socket.send("REGISTER:ACKSTATUS:2".encode())
                continue
            
            username = parts[1]
            password = parts[2]
            register_user(client_socket, username, password)
        
        elif message.startswith("ROOMLIST:"):
            if not logged_in_users:
                send_badauth(client_socket)
                continue
            
            parts = message.split(":")
            if len(parts) != 2:
                client_socket.send("ROOMLIST:ACKSTATUS:1".encode())
                continue
            
            mode = parts[1]
            room_list(client_socket, mode)
        
        else:
            send_badauth(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen(5)
    print("Server is listening on port 9999...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
