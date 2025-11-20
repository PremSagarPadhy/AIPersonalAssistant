import subprocess
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import time
import wolframalpha
import pywhatkit
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

print("Loading your AI personal assistant - ZIRA :")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the email right now.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            speak("I didn't catch that, please say it again.")
            return takeCommand()
        except sr.RequestError:
            speak("I'm having trouble connecting. Please try again later.")
            return "None"

def open_application(app_name, path):
    if shutil.which(app_name):
        os.startfile(path)
    else:
        speak(f"{app_name} is not installed on this system.")

if __name__ == "__main__":
    wishme()
    while True:
        speak("Please tell me, how may I help you?")
        query = takeCommand()
        
        if query in ["goodbye", "ok bye", "stop"]:
            speak("Your personal assistant Zira is shutting down. Goodbye!")
            break

        if "who are you" in query or "what can you do" in query:
            speak("I am Zira, your personal assistant. I can open applications, search Wikipedia, fetch the latest news, answer computational questions, and much more!")

        elif "who made you" in query:
            speak("I was built by Prem Sagar")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").strip()
            if query:
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are multiple results for this search. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("I couldn't find any information on Wikipedia.")
                except Exception as e:
                    speak("An error occurred while fetching data from Wikipedia.")
                    print(e)
            else:
                speak("Please provide a search term for Wikipedia.")

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            time.sleep(5)

        elif "open news" in query:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak("Here are some headlines from the Times of India.")
            time.sleep(5)

        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            time.sleep(5)

        elif "search" in query:
            query = query.replace("search", "")
            pywhatkit.search(query)
            time.sleep(5)

        elif "open stack overflow" in query:
            webbrowser.open_new_tab("https://stackoverflow.com")
            speak("Opening Stack Overflow...")
            
        elif "play music" in query:
            music_dir = r"C:\Users\sagar\Music\songs"
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("Music directory not found.")

        elif "the time" in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strtime}")

        elif "open chrome" in query:
            open_application("chrome", "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

        elif "open code" in query:
            open_application("code", "C:\\Users\\sagar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

        elif "email" in query:
            speak("What should I say?")
            content = takeCommand()
            sendEmail("sagarprempadhy@gmail.com", content)

        elif "ask" in query:
            speak("What question do you want to ask?")
            question = takeCommand()
            if question and question != "None":
                app_id = "VLTV58-PLHEU5AEWP"
                client = wolframalpha.Client(app_id)
                try:
                    res = client.query(question)
                    if res["pod"]:
                        answer = next(res.results).text
                        speak(answer)
                    else:
                        speak("Sorry, I couldn't find an answer to that.")
                except StopIteration:
                    speak("I'm not sure about that. Can you ask something else?")
                except Exception as e:
                    print("Error:", e)
                    speak("There was a problem getting the answer.")
            else:
                speak("I didn't hear a valid question.")
            
        elif "log off" in query or "sign out" in query:
                speak("Ok, your PC will log off in 10 seconds. Please save your work.")
                subprocess.call(["shutdown", "/l"])
        elif "hibernate" in query or "sleep mode" in query:
                speak("Hibernating your PC. Save all your work.")
                subprocess.call("shutdown /h", shell=True)