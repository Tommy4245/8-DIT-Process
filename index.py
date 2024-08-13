import sqlite3
import random
import time
import bcrypt

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
            users_choice = users_choice.upper() 
            if users_choice == option1 or users_choice == option2:  
                return users_choice
            else:
                print(invalid_select_option1_or_2)
        except:
            print(invalid_select_option1_or_2)

def string_input_validation_withmennu(msg, option1, option2, invalid_select_option1_or_2):
    print(msg)
    while True:
        users_choice = input(":")
        if users_choice == "0":
            menu(conn)
        users_choice = users_choice.upper() 
        if users_choice == option1 or users_choice == option2:  
            return users_choice
        else:
            print(invalid_select_option1_or_2)

def menu(conn):
    print("Remember, please type 0 to return to the menu at any time and remeber to remeber WordID's for your Wordlist!")
    print("Below are some options that you can return to:")
    print("Option 1: View a Random Japanese Word and Its Translation")
    print("Option 2: Practice your Wordlist")
    print("Option 3: Find New words to learn and Practice with sets")
    print("Option 4: Modify your Wordlist")
    print("Option 5: Exit")
    user_choice = number_input_validation("Please choose an option (1-5):", 1, 5)
    if user_choice == 1:
        view_random_word(conn)
    elif user_choice == 2:
        practice_wordlist(conn)
    elif user_choice == 3:
        learn(conn)
    elif user_choice == 4:
        user_add(conn)
    elif user_choice == 5:
        print("Please visit us again")
        conn.close()
        exit()

def user_add(conn):
    global current_user_id
    cursor = conn.cursor()
    cursor.execute('''SELECT Words.wordID, Words.word, Words.Romanji, Words.Translation, Words.Difficulty, Words.Genre 
                      FROM Words
                      JOIN Users_Wordlist ON Words.wordID = Users_Wordlist.wordID
                      WHERE Users_Wordlist.userID= ?''', (current_user_id,))
    words = cursor.fetchall()
    word_ids = [] 
    if words:
        print("Your wordlist:")
        for word in words:
            wordID, word, romanji, translation, difficulty, genre = word
            word_ids.append(wordID)
            print(f"\nWord ID: {wordID}")
            print(f"Japanese Word: {word}")
            print(f"Romanji: {romanji}")
            print(f"Translation: {translation}")
            print(f"Difficulty: {difficulty}")
            print(f"Genre: {genre}\n")
    else:
        print("Your wordlist is empty.")
    remove_or_add = string_input_validation_withmennu("Would you like to remove or add words to your Wordlist? |Remove/Add|", "REMOVE", "ADD", "Please type either remove or add")
    if remove_or_add == "ADD":
        word_id = number_input_validation("Please enter the Word ID you want to add to your wordlist that you have seen exploring this app: ", 1, 650)
        cursor.execute('SELECT * FROM Words WHERE wordID= ?', (word_id,))
        if cursor.fetchone():
            try:
                cursor.execute('INSERT INTO Users_Wordlist (userID, wordID) VALUES (?, ?)', (current_user_id, word_id))
                conn.commit()
                print("Word successfully added to your wordlist!")
            except sqlite3.IntegrityError as e:
                print(f"An error occurred: {e}")
        else:
            print("Invalid Word ID. The word does not exist.")
    elif remove_or_add == "REMOVE":
        word_id = number_input_validation("Please enter the Word ID you want to remove from your wordlist: ", 1, 650)
        if word_id in word_ids:
            try:
                cursor.execute('DELETE FROM Users_Wordlist WHERE userID = ? AND wordID = ?', (current_user_id, word_id))
                conn.commit()
                print("Word successfully removed from your wordlist!")
            except sqlite3.OperationalError as e:
                print(f"An error occurred: {e}")
        else:
            print("Invalid Word ID. Please enter a Word ID from your wordlist.")
    repeat = string_input_validation_withmennu("Would you like to Add/Remove any more words |Yes/No|", "YES", "NO","Invalid response, Please type either Yes or No")
    if repeat == "YES":
        user_add(conn)
    elif repeat == "NO":
        menu(conn)

def practice_wordlist(conn):
    global current_user_id
    cursor = conn.cursor()
    cursor.execute('''SELECT Words.wordID, Words.word, Words.Romanji, Words.Translation, Words.Difficulty, Words.Genre 
                      FROM Words
                      JOIN Users_Wordlist ON Words.wordID = Users_Wordlist.wordID
                      WHERE Users_Wordlist.userID = ?''', (current_user_id,))
    words = cursor.fetchall()
    if words:
        for word in words:
            wordid, word, romanji, translation, difficulty, genre = word
            print(f"\nWord ID: {wordid}")
            print(f"Japanese Word: {word}")
            print(f"Romanji: {romanji}")
            ans = input("Please type the translation: ")
            if ans.strip().lower() == translation.lower():
                print("Correct!")
            else:
                print(f"Incorrect! The correct translation is: {translation}")
            time.sleep(1)
        print("Practice session complete!")
    else:
        print("Your wordlist is empty.")
    menu(conn)

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
            print(f"Genre:\n",word[5])
            time.sleep(0.5)
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
        cursor.execute('SELECT * FROM Words WHERE Genre = ?', (chosen_genre,))
        words = cursor.fetchall()
        if words:
            for word in words:
                wordid, japanese_word, romanji, translation, difficulty, genre = word
                print(f"\nWord ID: {wordid}")
                print(f"Japanese Word: {japanese_word}")
                print(f"Romanji: {romanji}")
                ans = input("Please type the translation: ")
                if ans.strip().lower() == "0":
                    menu(conn)
                elif ans.strip().lower() == translation.lower():
                    print("Correct!")
                else:
                    print(f"Incorrect! The correct translation is: {translation}")
                time.sleep(1)
            print("Practice session complete!")
        else:
            print("No words found for the selected genre.")
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    menu(conn)

def learn(conn):
    print("Welcome to the Learning Area")
    print("Would you like to test your skills on sets or find new words to view or even practice your wordlist?")
    user_choice = number_input_validation("Please type 1 to test your skills on sets, type 2 to view New Words or type 3 to practice your wordlist",1,3)
    if user_choice == 1:
        learn_sets(conn)
    elif user_choice == 2:
        new_word(conn)
    elif user_choice == 3:
        practice_wordlist(conn)

def view_random_word(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM Words')
        words = cursor.fetchall()
        if words:
            words = random.choice(words)
            word_id, word, romanji, translation, difficulty, genre = words
            print(f"\nWord ID: {word_id}")
            print(f"Japanese Word: {word}")
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
            user_password = b"user_password"
            hashed = bcrypt.hashpw(user_password, bcrypt.gensalt())
            if (user_username, bcrypt.checkpw(user_password,hashed)) in credentials:
                print("Sign in successful!")
                cursor.execute('SELECT UserID FROM User_info WHERE Username = ?', (user_username,))
                current_user_id = cursor.fetchone()[0]
                menu(conn)
                break
            else:
                print("Invalid username or password. Please try again.")
    elif sign_create == "CREATE":
        user_name = input("What is your name: ")
        user_password = input("What would you like your password to be: ")
        user_password = b"user_password"
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
        