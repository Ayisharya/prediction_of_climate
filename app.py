import requests
import json
import speech_recognition as sr
import pyttsx3

# Gemini API Setup
API_KEY = "AIzaSyATwH943SZeBseHDCECEFJvBnvxFZpPjYU"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Function to get Gemini's reply
def chatbot_response(query):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": query}]}]}
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "I couldn't understand Gemini's reply."
    else:
        return f"Error {response.status_code}: {response.text}"

# Function to listen from microphone
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"🗣 You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Speech recognition service is down."

# Function to speak text directly
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

# Main loop
if __name__ == "__main__":
    print("🎙 Voice-enabled Gemini Chatbot started. Say 'exit' to quit.")
    while True:
        user_input = listen()
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("👋 Goodbye!")
            break
        bot_reply = chatbot_response(user_input)
        print(f"🤖 Gemini: {bot_reply}")
        speak(bot_reply)
