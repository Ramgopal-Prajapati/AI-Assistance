import openai
import speech_recognition as sr
import pyttsx3  # Text-to-speech library
import webbrowser
import subprocess  # Added for opening the music player
import smtplib     # Added for sending emails

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
api_key = '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'

# Initialize the OpenAI API client
openai.api_key = api_key

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the desired voice (you may need to install additional voices)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change to the desired voice

# Function to generate a response from GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=350  # Adjust this based on your requirements
    )
    return response.choices[0].text

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to open a music player (you can customize this)
def open_music_player():
    # Modify this to open your preferred music player
    subprocess.Popen(["your_music_player_command_here"])

# Function to send an email (you need to set up email credentials and recipients)
def send_email():
    smtp_server = "smtp.example.com"  # Replace with your SMTP server
    smtp_port = 587  # Replace with your SMTP port
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_email_password"  # Replace with your email password
    recipient_email = "recipient@example.com"  # Replace with the recipient's email

    subject = "Subject of your email"
    message = "Content of your email"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{message}")
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"An error occurred while sending the email: {str(e)}")

# Main loop for the chatbot
while True:
    with sr.Microphone() as source:
        print("Speak something:")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")

        if user_input.lower() == 'quit':
            speak("Goodbye!")
            break  # Exit the loop when the user says "quit"

        response = generate_response(user_input)
        print(f"Chatbot: {response}")

        speak(response)  # Speak the response

        # Check for specific commands
        if "open google" in response.lower():
            webbrowser.open("https://www.google.com")
        elif "open youtube" in response.lower():
            webbrowser.open("https://www.youtube.com")
        elif "open microsoft" in response.lower():
            webbrowser.open("https://www.microsoft.com")
        elif "open music player" in response.lower():
            open_music_player()
        elif "write email" in response.lower():
            send_email()

    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand what you said. Please try again.")
    except sr.RequestError:
        speak("Sorry, there was an error with the speech recognition service.")

print("Chatbot: Goodbye!")
