import speech_recognition as sr
import pyttsx3
import pandas as pd

# Initialize TTS engine once (performance kosam)
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the book name:")
        speak("Please say the book name")
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        speak("Please be patient, I am searching for it.")
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
    # CSV load cheyyadam
    df = pd.read_csv(file_path)

    # Case-insensitive search kosam lowercase title column add cheddam
    df["title_lower"] = df["title"].str.lower()

    # Binary search ki sort avvali title_lower meeda
    df = df.sort_values("title_lower").reset_index(drop=True)

    return df

def binary_search_book(book_name, books_df):
    """
    books_df must be sorted by 'title_lower'
    book_name -> string
    returns: matching row (Series) or None
    """
    target = book_name.lower()
    left = 0
    right = len(books_df) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_title = books_df.iloc[mid]["title_lower"]

        if mid_title == target:
            return books_df.iloc[mid]
        elif mid_title < target:
            left = mid + 1
        else:
            right = mid - 1

    return None

def check_availability(book_name, books_df):
    # Binary search use chesi book find cheyyadam
    result = binary_search_book(book_name, books_df)
    return result

# Integration
def main():
    books_df = load_books("F:\\B.tech\\mini_nila_50_books_database.csv")
    book_name = recognize_speech()

    if book_name:
        book = check_availability(book_name, books_df)

        if book is not None:
            if book["available"]:
                details = (
                    f"The book '{book['title']}' by {book['author']} is available.\n"
                    f"Description: {book['description']}."
                )
                print(details)
                speak(details)
                speak("Thank you. Happy reading.")
            else:
                msg = f"The book '{book_name}' is not available in our library."
                print(msg)
                speak(msg)
                speak("Thank you, have a nice day.")
        else:
            msg = f"The book '{book_name}' is not in our database."
            print(msg)
            speak(msg)
            speak("Thank you, have a nice day.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
