import os
import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

def query(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def generate_caption(image_path):
    output = query(image_path)
    if isinstance(output, list) and len(output) > 0:
        return output[0]['generated_text']
    else:
        return "Error: Unable to generate caption."

class ImageCaptioningApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Captioning")

        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.caption_label = tk.Label(master, wraplength=300, justify="center")
        self.caption_label.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.display_image_and_caption(file_path)

    def display_image_and_caption(self, image_path):
        # Display the image
        image = Image.open(image_path)
        image.thumbnail((300, 300))  # Resize image for display
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference

        # Generate and display the caption
        caption = generate_caption(image_path)
        self.caption_label.config(text=f"Caption: {caption}")

# Create the main window
root = tk.Tk()
app = ImageCaptioningApp(root)
root.mainloop()
