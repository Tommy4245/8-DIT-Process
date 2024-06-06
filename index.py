import sqlite3
import random


conn = sqlite3.connect('8DIT_Database.db')
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
    print("Option 2: Exit")
    
    user_choice = number_input_validation("Please choose an option (1-2):", 1, 2)
    if user_choice == 1:
        view_random_word(conn)
    elif user_choice == 2:
        print("Please visit us again")
        conn.close()
        exit()

def view_random_word(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Words")
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
