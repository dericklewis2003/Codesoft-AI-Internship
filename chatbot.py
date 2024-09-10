import re
import requests
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext

# Load environment variables from .env file
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

def query_huggingface(payload):
    if isinstance(payload, dict) and 'inputs' in payload:
        payload = payload['inputs']
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def simple_chatbot(user_input):
    user_input_lower = user_input.lower()

    rules = [
        (r'\b(hi|hello|hey)\b', "Hello! How can I help you today?"),
        (r'\bhow are you\b', "I'm doing well, thank you for asking!"),
        (r'\bweather\b', "I'm sorry, I don't have real-time weather information. You might want to check a weather app or website."),
        (r'\b(bye|goodbye)\b', "Goodbye! Have a great day!"),
        (r'\bname\b', "My name is ChatBot. It's nice to meet you!"),
        (r'\b(thanks|thank you)\b', "You're welcome! Is there anything else I can help you with?"),
        (r'\bhelp\b', "I'm here to assist you. You can ask me simple questions or just chat with me.")
    ]

    for pattern, response in rules:
        if re.search(pattern, user_input_lower):
            return response

    try:
        api_response = query_huggingface(user_input)
        
        if isinstance(api_response, dict) and 'error' in api_response:
            return f"An error occurred: {api_response['error']}"
        
        if isinstance(api_response, list) and len(api_response) > 0:
            generated_text = api_response[0].get('generated_text', '')
        else:
            generated_text = ''
        
        return generated_text.strip()
    except Exception as e:
        return f"I apologize, but I'm having trouble generating a response right now. Error: {str(e)}"

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")
        master.geometry("400x500")

        self.chat_history = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=25)
        self.chat_history.pack(padx=10, pady=10)
        self.chat_history.config(state=tk.DISABLED)

        self.user_input = tk.Entry(master, width=50)
        self.user_input.pack(padx=10, pady=5)
        self.user_input.bind("<Return>", self.send_message)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        self.send_button = tk.Button(button_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = tk.Button(button_frame, text="Quit", command=self.quit_app)
        self.quit_button.pack(side=tk.LEFT, padx=5)

        self.display_message("ChatBot: Hello! I'm a chatbot. How can I help you today?")

    def display_message(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip() != "":
            self.display_message(f"You: {user_message}")
            self.user_input.delete(0, tk.END)

            bot_response = simple_chatbot(user_message)
            self.display_message(f"ChatBot: {bot_response}")

            if user_message.lower() == 'bye':
                self.master.after(1000, self.quit_app)

    def quit_app(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()
