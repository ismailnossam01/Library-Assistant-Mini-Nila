import speech_recognition as sr
import pyttsx3
import pandas as pd

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:       
        print("Please say the book name:")
        speak("Please say the book name")
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        speak("Please be patience i am searching for it .")
        book_name = recognizer.recognize_google(audio)
        print(f"You said: {book_name}")
        return book_name
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        speak("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return None

def load_books(file_path):
    return pd.read_csv(file_path)


def check_availability(book_name, books_df):
    book = books_df[books_df['title'].str.lower() == book_name.lower()]
    return book


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Step 5: Integration
def main():
    books_df = load_books("F:\\B.tech\\mini_nila_50_books_database.csv")
    book_name = recognize_speech()
    if book_name:
        book_details = check_availability(book_name, books_df)
        if not book_details.empty:
            book = book_details.iloc[0]
            if book['available']:
                details = (f"The book '{book['title']}' by {book['author']} is available. \n"
                           f"Description: {book['description']}.")
                print(details)
                speak(details)
                speak("Thank you Happy Reading .")

            else:
                print(f"The book '{book_name}' is not available in our library.")
                speak(f"The book '{book_name}' is not available in our library.")
                speak("Thank you have a nice day .")

        else:
            print(f"The book '{book_name}' is not in our database.")
            speak(f"The book '{book_name}' is not in our database.")
            speak("Thank you have a nice day .")

    
    input()
if __name__ == "__main__":
    main()
