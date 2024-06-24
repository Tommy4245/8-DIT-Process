import sqlite3
import random
import time

difficulty_list = ["Beginner","Intermediate","Advanced"]
genre_list = ["Phrase","Daily Life","Business","Numbers","Colors","Travel","Basic Words","Verbs","Food and Dining","Education","Health and Body","Weather and Nature","Travel and Transportation","Shopping and Money","Food and Dining","Sports and Recreation","Travel and Places","Technology","Environment","Entertainment"]

conn = sqlite3.connect('Database.db')
cursor = conn.cursor()

def number_input_validation(msg, minimum, maximum):
    """Validate int values that the user has selected and has boundaries to validate the user response is in range."""
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

def menu(conn):
    print("\nWelcome To This Japanese Language Learning App")
    print("Below are some options that you can return to:")
    print("Option 1: View a Random Japanese Word and Its Translation")
    print("Option 2: View your Wordlist")
    print("Option 3: Find New words to learn and Practice with sets")
    print("Option 4: Exit")
    
    user_choice = number_input_validation("Please choose an option (1-4):", 1, 4)
    if user_choice == 1:
        view_random_word(conn)
    elif user_choice == 2:
        ...
    elif user_choice == 3:
        learn(conn)
    elif user_choice == 4:
        print("Please visit us again")
        conn.close()
        exit()

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
    menu(conn)