import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import smtplib
from email.mime.text import MIMEText
from transformers import pipeline

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# ✅ Correct HuggingFace pipeline initialization
nlp = pipeline("text-generation", model="google/flan-t5-base")

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please repeat.")
        return None

def tell_time():
    now = datetime.datetime.now()
    speak(f"The time is {now.strftime('%H:%M')} and date is {now.strftime('%d %B %Y')}")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {query}")

def get_weather(city="Delhi"):
    api_key = "615000e6c82354862fa9844221eaeb80"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with {temp} degree Celsius")
    else:
        speak("Sorry, I couldn't fetch the weather right now.")

def send_email(to, subject, body):
    sender = "sakshipal1512007@gmail.com"
    password = "Purvi#2007"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to, msg.as_string())
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print(e)

def process_command(query):
    if "hello" in query:
        speak("Hello Sakshi! How can I help you today?")
    elif "time" in query or "date" in query:
        tell_time()
    elif "search" in query:
        topic = query.replace("search", "").strip()
        search_web(topic)
    elif "weather" in query:
        city = query.replace("weather", "").strip() or "Delhi"
        get_weather(city)
    elif "email" in query:
        send_email("receiver@example.com", "Test Subject", "This is a test email from your assistant.")
    else:
    # Use text-generation for general queries
        result = nlp(query, max_length=100)
        answer = result[0]["generated_text"]
        speak(answer)


# Main loop
if __name__ == "__main__":
    speak("Voice Assistant Online. Say something...")
    while True:
        query = listen()
        if query:
            if "exit" in query or "quit" in query:
                speak("Goodbye Sakshi!")
                break
            process_command(query)
