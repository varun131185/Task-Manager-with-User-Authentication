import hashlib
import os
import csv

import UserTaskManger

# Global file name for storing username and password info
USER_FILE = 'users_info/users.csv'

# Global list to store user's info
users = []


# ---------- private method : hashing of password before storing in file ------------ #
def _hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# ------------------ Save & Load Users ------------------ #
def load_users(filename="users.csv"):
    global users
    file_path = "users_info/" + filename
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            users = [row for row in reader]
        print("Users Information loaded successfully.")
    else:
        users = []
        print("There is no Users Information Available.")


# private method
def _save_user(username, pwd, filename="users.csv"):
    global users
    new_user = []
    # creating user as dictionary
    user = {
        'USERNAME': username,
        'PASSWORD': pwd
    }
    # adding new user to existing user list
    users.append(user)
    # adding user as dictionary in new user list to write in file
    new_user.append(user)
    file_path = "users_info/" + filename
    directory_path = "users_info/"
    os.makedirs(directory_path, exist_ok=True)
    if os.path.exists(file_path):
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['USERNAME', 'PASSWORD'])
            # Write the new row to the CSV file
            writer.writerows(new_user)
            file.close()
    else:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['USERNAME', 'PASSWORD'])
            # Write the new row to the CSV file
            writer.writeheader()
            writer.writerows(new_user)
            file.close()


# ------------------ Register User ------------------ #
def register():
    while True:
        username = input("Enter a new username: ").strip()
        userinfo = next((uf for uf in users if uf.get("USERNAME") == username), None)
        if not username:
            print("Username cannot be empty.")
        elif userinfo is not None:
            print("Username already exists. Please choose a different one.")
        else:
            break
    while True:
        password = input("Enter a password: ")
        if not password:
            print("Password cannot be empty.")
        else:
            break
    pwd_hash = _hash_password(password)
    _save_user(username=username, pwd=pwd_hash)
    print("Registration successful!\n")


# ------------------ Login User ------------------ #
def login():
    global users
    username = input("Username: ").strip()
    # Find dictionary entry where 'username' match
    userinfo = next((uf for uf in users if uf.get("USERNAME") == username), None)
    if userinfo is not None:
        password = input("Password: ")
        if userinfo.get("PASSWORD") == _hash_password(password):
            print("Login successful! Access granted to task manager.\n")
            task_manager = UserTaskManger.UserTaskManger(username)
            task_manager.interactive_task_menu()
        else:
            print("Password is incorrect.\n")
    else:
        print("Invalid username.\n")


# ------------------ Interactive menu ------------------ #
def interactive_user_menu():
    # Load all users details on start
    load_users()
    while True:
        print("\n==== User Authentication ====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option! Please choose between 1 and 3.")


# ------------------ Run the program ------------------ #
if __name__ == "__main__":
    interactive_user_menu()
