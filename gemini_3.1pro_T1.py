import hashlib
import sys

# In-memory database to store credentials. 
# Format: {"username": "hashed_password"}
users_db = {}

def hash_password(password):
    """
    Hashes a password using SHA-256.
    Returns the hexadecimal representation of the hash.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register():
    """Handles new user registration."""
    print("\n--- Register ---")
    username = input("Enter a new username: ").strip()
    
    if not username:
        print("Username cannot be empty.")
        return
        
    if username in users_db:
        print("Error: Username already exists. Please try logging in or pick a different name.")
        return
        
    password = input("Enter a password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
        
    # Store the hashed version of the password, NEVER the plain text
    users_db[username] = hash_password(password)
    print(f"Success! User '{username}' has been registered.")

def login():
    """Handles existing user login."""
    print("\n--- Login ---")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    # Check if the user exists
    if username not in users_db:
        print("Error: Username not found.")
        return
        
    # Hash the inputted password and compare it to the stored hash
    input_hash = hash_password(password)
    stored_hash = users_db[username]
    
    if input_hash == stored_hash:
        print(f"Success! Welcome back, {username}.")
    else:
        print("Error: Incorrect password.")

def main():
    """Main menu loop for the application."""
    while True:
        print("\n=== Main Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Please select an option (1-3): ").strip()
        
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()