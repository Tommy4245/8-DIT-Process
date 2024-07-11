import sqlite3
import random
import time

difficulty_list = ["Beginner","Intermediate","Advanced"]
genre_list = ["Phrase","Daily Life","Business","Numbers","Colors","Travel","Basic Words","Verbs","Food and Dining","Education","Health and Body","Weather and Nature","Travel and Transportation","Shopping and Money","Food and Dining","Sports and Recreation","Travel and Places","Technology","Environment","Entertainment"]

conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

def number_input_validation(msg, minimum, maximum):
    print(msg)
    while True:
        try:
            user_response = int(input(":"))
            if user_response == 0:  
                menu(conn)
                user_add(conn)
            elif minimum <= user_response <= maximum:
                return user_response
            else:
                print("That item is not in range")
        except ValueError:
            print("Invalid answer, please make sure to choose a number between", minimum, "-", maximum)

def string_input_validation(msg, option1, option2, invalid_select_option1_or_2):
    print(msg)
    while True:
        try:
            users_choice = input(":")
            users_choice = users_choice.upper()  # Formats so all the results have the same case to avoid confusion and errors makeing my program Robust
            if users_choice == option1 or users_choice == option2:  # Checks to see if the User has inputed a Valid choice
                return users_choice
            else:
                print(invalid_select_option1_or_2)
        except:
            print(invalid_select_option1_or_2)

def menu(conn):
    print("Remember, please type 0 to return to the menu at any time and remeber to remeber WordID's for your Wordlist!")
    print("Below are some options that you can return to:")
    print("Option 1: View a Random Japanese Word and Its Translation")
    print("Option 2: View your Wordlist")
    print("Option 3: Find New words to learn and Practice with sets")
    print("Option 4: Exit")
    
    user_choice = number_input_validation("Please choose an option (1-5):", 1, 5)
    if user_choice == 1:
        view_random_word(conn)
    elif user_choice == 2:
        ...
    elif user_choice == 3:
        learn(conn)
    elif user_choice == 4:
        user_add(conn)
    elif user_choice == 5:
        print("Please visit us again")
        conn.close()
        exit()

def user_add(word):
    global current_user_id
    word_id = int(input("Please enter the Word ID you want to add to your wordlist: "))
    
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users_Wordlist (user_id, word_id) VALUES (?, ?)', (current_user_id, word_id))
        conn.commit()
        print("Word successfully added to your wordlist!")
    except sqlite3.IntegrityError as e:
        print(f"An error occurred: {e}")

    
    
def new_word(conn):
    print("Choose a difficulty:")
    for i, diff in enumerate(difficulty_list, start =1):
        print(f"{i}. {diff}")
    diff_choice = number_input_validation("Please choose a difficulty (1-3):", 1, 3)
    chosen_diff = difficulty_list[diff_choice - 1]
    print("Choose a genre:")
    for i, gen in enumerate(genre_list, start=1):
        print(f"{i}. {gen}")
    gen_choice = number_input_validation(f"Please choose a genre (1-{len(genre_list)}):", 1, len(genre_list))
    chosen_genre = genre_list[gen_choice - 1]
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM Words where Genre =? and Difficulty =?',(chosen_genre,chosen_diff))
        words = cursor.fetchall()
        for word in words:
            print(f"\nWord ID:",word[0])
            print(f"Japanese Word:",word[1])
            print(f"Romanji:",word[2])
            print(f"Translation:",word[3])
            print(f"Difficulty:",word[3])
            print(f"Genre:",word[5])
        else:
            print("Sorry, No sets found with your specific requirments")
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    print("Please memorise the Words above, I will now return you to the Menu to make your next descion")
    menu(conn)

def learn_sets(conn):
    print("Welcome to the sets learning area")
    print("Please choose a genre:")
    for i, gen in enumerate(genre_list, start=1):
        print(f"{i}. {gen}")
    gen_choice = number_input_validation(f"Please choose a genre (1-{len(genre_list)}):", 1, len(genre_list))
    chosen_genre = genre_list[gen_choice - 1]
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM Words where Genre =?',(chosen_genre,))
        words = cursor.fetchall()
        for word in words:
            print(f"\nWord ID:",word[0])
            print(f"Japanese Word:",word[1])
            print(f"Romanji:",word[2])
            print(f"Genre:",word[5])
            ans = 0
            ans = number_input_validation("Please type 1 when you want/believe you have the anwser",1,1)
            if ans == 1:
                print(f"Translation:",word[3])
                time.sleep(1)
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    print("Set Complete, returning to menu")
    menu(conn)

def learn(conn):
    print("Welcome to the Learning Area")
    print("Would you like to test your skills on sets or find new words to view?")
    user_choice = number_input_validation("Please type 1 to test your skills on sets, and type 2 to view New Words",1,2)
    if user_choice == 1:
        learn_sets(conn)
    elif user_choice == 2:
        new_word(conn)

def view_random_word(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM Words')
        words = cursor.fetchall()
        if words:
            words = random.choice(words)
            word_id, japanese_word, romanji, translation, difficulty, genre = words
            print(f"\nWord ID: {word_id}")
            print(f"Japanese Word: {japanese_word}")
            print(f"Romanji: {romanji}")
            print(f"Translation: {translation}")
            print(f"Difficulty: {difficulty}")
            print(f"Genre: {genre}\n")
        else:
            print("No words found in the database.")
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    menu(conn)

if __name__ == "__main__":
    print("\nWelcome To This Japanese Language Learning App")
    sign_create = string_input_validation("Please sign in or create an account, type sign to sign in or create to create an account: ","CREATE","SIGN","Invalid response please choose either create or sign")
    if sign_create == "SIGN":
        cursor.execute('SELECT Username, Users_Password FROM User_info')
        credentials = cursor.fetchall()
        user_username = ""
        while True:
            user_username = input("Please enter username: ")
            user_password = input("Please enter password: ")
            if (user_username, user_password) in credentials:
                print("Sign in successful!")
                cursor.execute('SELECT UserID FROM User_info WHERE Username = ?', (user_username,))
                current_user_id = cursor.fetchone()[0]
                menu(conn)
                break
            else:
                print("Invalid username or password. Please try again.")
    elif sign_create == "CREATE":
        user_name = input("What is your name so I can track your words: ")
        user_password = input("What would you like your password to be: ")
        cursor.execute('SELECT Username FROM User_info')
        usernames = [row[0] for row in cursor.fetchall()]
        user_username = ""
        while user_username == "" or user_username in usernames:
            user_username = input("Please choose a username: ")
            if user_username in usernames:
                print("Username already taken, please choose another one.")
        cursor.execute('INSERT INTO User_info (Username, Users_Password, User_Name) VALUES (?, ?, ?)', (user_username, user_password, user_name))
        conn.commit()
        print("Account created successfully!")
        menu(conn)