#Imports functions to connect the database, time functions, encryption functions and random functions 
import sqlite3
import random
import time
import bcrypt

#Lists that contain both the Genres and Difficulty of words
difficulty_list = ["Beginner","Intermediate","Advanced"]
genre_list = ["Phrase","Daily Life","Business","Numbers","Colors","Travel","Basic Words","Verbs","Food and Dining","Education","Health and Body","Weather and Nature","Travel and Transportation","Shopping and Money","Food and Dining","Sports and Recreation","Travel and Places","Technology","Environment","Entertainment"]

# Establishes the link the SQL Database
conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

#Int input Validation
def number_input_validation(msg, minimum, maximum):
    print(msg)
    while True:
        try:
            user_response = int(input(":"))
            if user_response == 0:  
                menu(conn)
            elif minimum <= user_response <= maximum:
                return user_response
            else:
                print("That item is not in range")
        except ValueError:
            print("Invalid answer, please make sure to choose a number between", minimum, "-", maximum)

#String input validation that is used for the Login area
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

#String input validation used for the rest of the code
def string_input_validation_withoutmennu(msg, option1, option2, invalid_select_option1_or_2):
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

#menu function 
def menu(conn):
    print("")
    print("Remember, please type 0 to return to the menu at any time and remeber to remeber WordID's for your Wordlist!")
    print("Below are some options that you can return to:")
    print("Option 1: View a Random Japanese Word and Its Translation")
    print("Option 2: Practice your Wordlist")
    print("Option 3: Find New words to learn and Practice with sets")
    print("Option 4: Modify your Wordlist")
    print("Option 5: Exit")
#options the user is supplied with
    user_choice = number_input_validation("Please choose an option (1-5):", 1, 5)
    if user_choice == 1:
        view_random_word(conn)
    elif user_choice == 2:
        practice_wordlist(conn)
    elif user_choice == 3:
        learn(conn)
    elif user_choice == 4:
        user_add_remove_choice(conn)
    elif user_choice == 5:
        print("Please visit us again")
        conn.close()
        exit()

#Function that gives the user the choice to either Add or Remove data from there wordlist
def user_add_remove_choice(conn):
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
        add_or_remove = string_input_validation_withoutmennu("Would you like to ADD or REMOVE words from your wordlist, please type either 'add' or 'remove' |Add/Remove|","ADD","REMOVE","Please type either Add or Remove")
        if add_or_remove == "ADD":
            add(conn)
        elif add_or_remove == "REMOVE":
            remove(conn)
    else:
        add_or_menu = string_input_validation_withoutmennu("Your wordlist is empty so you can only Add words, would you like to do this |Yes/No|","YES","NO","Please type either Yes or No")
        if add_or_menu == "YES":
            add(conn)
        elif add_or_menu == "NO":
            print("Returning to Menu")
            menu(conn)
    
#Function that adds word to the Users Wordlist
def add(conn):
    word_id = number_input_validation("Please enter the Word ID you want to add to your wordlist that you have seen exploring this app: ", 1, 650)
    cursor.execute('SELECT * FROM Words WHERE wordID= ?', (word_id,))
    if cursor.fetchone():
        try:
#sends data to the users wordlist
            cursor.execute('INSERT INTO Users_Wordlist (userID, wordID) VALUES (?, ?)', (current_user_id, word_id))
            conn.commit()
            print("Word successfully added to your wordlist!")
        except sqlite3.IntegrityError as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid Word ID. The word does not exist.")
    print("Returning to Menu so You can learn")
    menu(conn)

#Function that Removes words from the Users Wordlist
def remove(conn):
    global current_user_id
    cursor = conn.cursor()
    cursor.execute('''SELECT Words.wordID, Words.word, Words.Romanji, Words.Translation, Words.Difficulty, Words.Genre 
                      FROM Words
                      JOIN Users_Wordlist ON Words.wordID = Users_Wordlist.wordID
                      WHERE Users_Wordlist.userID= ?''', (current_user_id,))
    words = cursor.fetchall()
    word_ids = [] 
    if words:
        for word in words:
            wordID = word
            word_ids.append(wordID)
    word_id = number_input_validation("Please enter the Word ID you want to remove from your wordlist: ", 1, 650)
    if word_id in word_ids[0]:
        try:
#Removes words from the Users wordlist
            cursor.execute('DELETE FROM Users_Wordlist WHERE userID = ? AND wordID = ?', (current_user_id, word_id))
            conn.commit()
            print("Word successfully removed from your wordlist!")
        except sqlite3.OperationalError as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid Word ID. Please enter a Word ID from your wordlist.")
    print("Returning to Menu so You can learn")
    menu(conn)

#Function that allows the User to practice there wordlist
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
#Tests the users knowledge on there wordlist
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

#Function that lets the user see multiple new words by selecting a difficulty and genre
def new_word(conn):
    print("")
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
        if len(words) != 0:
            for word in words:
#Prints out all the words
                print(f"\nWord ID:",word[0])
                print(f"Japanese Word:",word[1])
                print(f"Romanji:",word[2])
                print(f"Translation:",word[3])
                print(f"Difficulty:",word[4])
                print(f"Genre:",word[5])
#Sleep function spaces each word getting printed out so the user can read them 
                time.sleep(0.5)
        elif len(words) == 0:
            print("Sorry, No sets found with your specific requirments")   
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    print("Please memorise the Words above, I will now return you to the Menu to make your next descion")
    menu(conn)

#Function tests the users knowledge on sets
def learn_sets(conn):
    print("")
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
#Prints out words then tests the Users ability to answer the Question
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

#A general function in which the user can selesct how they want to learn, if its by practicing therewordlist, by sets, or by new words
def learn(conn):
    print("")
    print("Welcome to the Learning Area")
    print("Would you like to test your skills on sets or find new words to view or even practice your wordlist?")
    user_choice = number_input_validation("Please type 1 to test your skills on sets, type 2 to view New Words or type 3 to practice your wordlist",1,3)
    if user_choice == 1:
        learn_sets(conn)
    elif user_choice == 2:
        new_word(conn)
    elif user_choice == 3:
        practice_wordlist(conn)

#Basic function which allows the user to view a random word
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

#Sign in menu for the user on start up
if __name__ == "__main__":
    print("\nWelcome To This Japanese Language Learning App")
    sign_create = string_input_validation("Please sign in or create an account, type sign to sign in or create to create an account: ","CREATE","SIGN","Invalid response please choose either create or sign")
    if sign_create == "SIGN":
        cursor.execute('SELECT Username, Users_Password FROM User_info')
        user_username = ""
        while True:
#Asks the user for credentials
            user_username = input("Please enter username: ")
            user_password = input("Please enter password: ").encode('utf-8')
            cursor.execute('SELECT Users_Password FROM User_info WHERE Username = ?', (user_username,))
            result = cursor.fetchone()
            if result:
#Checks hashed and salted password = users input
                stored_password_hash = result[0]
                if isinstance(stored_password_hash, str):
                    stored_password_hash = stored_password_hash.encode('utf-8')
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
#Gets the users infomation
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
#Sends the users hashed and salted password and username into my database
        cursor.execute('INSERT INTO User_info (Username, Users_Password, User_Name) VALUES (?, ?, ?)', (user_username, hashed, user_name))
        conn.commit()
        print("Account created successfully!")
        cursor.execute('SELECT userID FROM User_info WHERE Username = ?', (user_username,))
        current_user_id = cursor.fetchone()[0]
        menu(conn)