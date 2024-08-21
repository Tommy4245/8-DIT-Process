import sqlite3
import bcrypt

# Connect to the database
conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

# Fetch user credentials
username = '123'
password = b'123'

cursor.execute('SELECT Username, Users_Password FROM User_info WHERE Username = ?', (username,))
user_record = cursor.fetchone()

if user_record:
    stored_username, stored_hashed_password = user_record
    
    # Verify the password
    if bcrypt.checkpw(password, stored_hashed_password):
        print("Password match")
    else:
        print("Password does not match")
else:
    print("User not found")

conn.close()







if __name__ == "__main__":
    print("\nWelcome To This Japanese Language Learning App")
    sign_create = string_input_validation("Please sign in or create an account, type sign to sign in or create to create an account: ","CREATE","SIGN","Invalid response please choose either create or sign")
    if sign_create == "SIGN":
        cursor.execute('SELECT Username, Users_Password FROM User_info')
        user_username = ""
        while True:
            user_username = input("Please enter username: ")
            user_password = input("Please enter password: ").encode('utf-8')
            
            cursor.execute('SELECT Users_Password FROM User_info WHERE Username = ?', (user_username,))
            result = cursor.fetchone()
            
            if result:
                stored_password_hash = result[0]
                if isinstance(stored_password_hash, str):
                    stored_password_hash = stored_password_hash.encode('utf-8')
                
                print(f"Stored hash: {stored_password_hash}")
                print(f"Stored hash type: {type(stored_password_hash)}")
                print(f"Entered password (encoded): {user_password}")
                
                if bcrypt.checkpw(user_password, stored_password_hash):
                    print("Sign in successful!")
                    cursor.execute('SELECT UserID FROM User_info WHERE Username = ?', (user_username,))
                    current_user_id = cursor.fetchone()[0]
                    menu(conn)
                    break
                else:
                    print("Invalid password. Please try again.")
            else:
                print("Invalid username. Please try again.")

    elif sign_create == "CREATE":
        user_name = input("What is your name: ")
        user_password = input("What would you like your password to be: ").encode('utf-8')
        hashed = bcrypt.hashpw(user_password, bcrypt.gensalt())
        cursor.execute('SELECT Username FROM User_info')
        usernames = [row[0] for row in cursor.fetchall()]
        user_username = ""
        while user_username == "" or user_username in usernames:
            user_username = input("Please choose a username: ")
            if user_username in usernames:
                print("Username already taken, please choose another one.")
        cursor.execute('INSERT INTO User_info (Username, Users_Password, User_Name) VALUES (?, ?, ?)', (user_username, hashed, user_name))
        conn.commit()
        print("Account created successfully!")
        cursor.execute('SELECT userID FROM User_info WHERE Username = ?', (user_username,))
        current_user_id = cursor.fetchone()[0]
        menu(conn)