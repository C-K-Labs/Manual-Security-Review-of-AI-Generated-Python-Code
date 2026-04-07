import sqlite3

class UserDatabase:
    def __init__(self, db_name="users.db"):
        """Initializes the connection and creates the table if it doesn't exist."""
        # Note: Use ":memory:" for a temporary in-RAM database, 
        # or a filename like "users.db" to save to disk.
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates the users table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        ''')
        self.conn.commit()

    def add_user(self, name, email, age):
        """Creates a new user (Create)."""
        try:
            self.cursor.execute('''
                INSERT INTO users (name, email, age)
                VALUES (?, ?, ?)
            ''', (name, email, age))
            self.conn.commit()
            print(f"SUCCESS: User '{name}' added.")
        except sqlite3.IntegrityError:
            print(f"ERROR: A user with the email '{email}' already exists.")

    def get_user(self, user_id):
        """Fetches a single user by ID (Read)."""
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()

    def get_all_users(self):
        """Fetches all users from the database (Read)."""
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def update_user(self, user_id, name, email, age):
        """Updates an existing user's information (Update)."""
        self.cursor.execute('''
            UPDATE users
            SET name = ?, email = ?, age = ?
            WHERE id = ?
        ''', (name, email, age, user_id))
        self.conn.commit()
        
        if self.cursor.rowcount > 0:
            print(f"SUCCESS: User ID {user_id} updated.")
        else:
            print(f"ERROR: User ID {user_id} not found.")

    def delete_user(self, user_id):
        """Deletes a user by ID (Delete)."""
        # First, let's grab the name just so we can print a nice confirmation
        self.cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        user = self.cursor.fetchone()
        
        if user:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.conn.commit()
            print(f"SUCCESS: User '{user[0]}' (ID {user_id}) deleted.")
        else:
            print(f"ERROR: User ID {user_id} not found.")

    def close(self):
        """Closes the database connection."""
        self.conn.close()


# ==========================================
# Demonstration Block
# ==========================================
if __name__ == "__main__":
    # Initialize the database. 
    # Using ":memory:" creates a fresh database in RAM every time you run the script.
    # To save your data permanently, change this to a filename, e.g., db = UserDatabase("my_users.db")
    db = UserDatabase(":memory:") 

    print("--- 1. CREATING USERS ---")
    db.add_user("Alice Smith", "alice@example.com", 28)
    db.add_user("Bob Jones", "bob@example.com", 35)
    db.add_user("Charlie Brown", "charlie@example.com", 22)
    db.add_user("Duplicate Alice", "alice@example.com", 30) # This will fail due to the UNIQUE constraint

    print("\n--- 2. READING USERS ---")
    print("All Users:")
    for user in db.get_all_users():
        print(f"  {user}")

    print("\nSingle User (ID: 2):")
    print(f"  {db.get_user(2)}")

    print("\n--- 3. UPDATING USER ---")
    db.update_user(2, "Robert Jones", "robert.j@example.com", 36)
    print(f"Updated User (ID: 2): {db.get_user(2)}")

    print("\n--- 4. DELETING USER ---")
    db.delete_user(3)
    db.delete_user(99) # Testing a non-existent user

    print("\n--- FINAL DATABASE STATE ---")
    for user in db.get_all_users():
        print(f"  {user}")

    # Clean up
    db.close()