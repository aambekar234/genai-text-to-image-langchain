"""
Author: Abhijeet Ambekar
Data: 01/01/2024
Website: https://www.linkedin.com/in/aambekar234/
"""

import os
import tkinter
from tkinter import Toplevel, Label, Button, StringVar, ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
from langchain.chat_models import ChatOpenAI
from main import create_sequential_chain
from main import generate_image
import openai
import requests, threading
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY')
font_size = 14
bg_color = '#333333'
window = tkinter.Tk()
window.configure(bg=bg_color)
window.title("App by A. Ambekar")
window.geometry('800x520')
frame = tkinter.Frame(bg=bg_color)

def fetch_image(popupFrame, popupWindow, temperature, user_text, model):
    """
    Fetches an image from a URL and displays it along with the generated prompt text.

    Args:
        popupFrame (tkinter.Frame): The frame to display the image and text.
        popupWindow (tkinter.Tk): The window to display the frame.
        temperature (float): The temperature value for generating the prompt.
        user_text (str): The user input text.
        model: The model used for generating the prompt.

    Returns:
        None
    """
    try:
        result_textbox = tkinter.Text(popupFrame, height=30, width=100, bg='#333333', fg="#FFFFFF",  font=("Arial", font_size-2))
        
        progress = ttk.Progressbar(popupFrame, orient='horizontal', mode='indeterminate')
        progress.place(x=0, y=0, width=50, height=20)
        progress.start(5)
        progress.grid(row=0, column=0, sticky="news", pady=200, padx=10)
        popupFrame.pack()
        
        
        model = ChatOpenAI(temperature=temperature, model=selected_model.get())
        reposne = create_sequential_chain(model, user_text)
        image_prompt = reposne["final_prompt"]
        url, revised_prompt = generate_image(image_prompt)
        
        text = f"Image URL\n{url}\n\nGenerated Prompt\n{image_prompt}\n\nDall.e-3 Revised Prompt\n{revised_prompt}"
        
        # Fetch the image from URL
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img.thumbnail((800, 400))
        popupWindow.title("Results")
    except Exception as e:
        popupWindow.title("Error")
        print("Exception: ", e )
        img = Image.open('images/error.png')
        img.thumbnail((200, 200))
        text = "Something went wrong. Please check the console logs for more details."
    
    progress.grid_forget()
    result_textbox.insert(tkinter.INSERT, text)
    img_tk = ImageTk.PhotoImage(img)
    # Update the label to display the image
    img_label = Label(popupFrame, image=img_tk)
    img_label.image = img_tk
    img_label.grid(row=0, column=0, sticky="news", pady=5)
    result_textbox.grid(row=1, column=0, sticky="news", pady=10, padx=10)
    popupFrame.pack()

def create_fetch_window():
    """
    Creates a fetch window and starts fetching in a new thread.

    This function retrieves the temperature value, user text, and selected model from the GUI.
    It performs input validation and displays error messages if necessary.
    If the input is valid, it creates a new window and starts fetching the image in a new thread.

    Args:
        None

    Returns:
        None
    """
    temperature = float(temperature_entry.get())
    user_text = textbox_entry.get("1.0", "end-1c")
    print(temperature, user_text, selected_model.get())
    
    
    if temperature < 0.0 or temperature > 0.9:
        messagebox.showerror(title="Error", message="Invalid temperature value")
        return
    if not user_text:
        messagebox.showerror(title="Error", message="Text box is empty")
        return
    
    # Create a new window
    new_window = Toplevel()
    new_window.geometry('950x800')
    new_window.title("Generating...")
    new_frame = tkinter.Frame(new_window, bg='#333333')
    
    # Start fetching in a new thread
    threading.Thread(target=fetch_image, args=(new_frame, new_window, temperature, user_text, selected_model.get())).start()




# Creating widgets
screen_label = tkinter.Label(
    frame, text="Text to Immersive Picture", bg='#333333', fg="#FF3399", font=("Arial", 25))

textbox_label = tkinter.Label(
    frame, text="Enter your text", bg='#333333', fg="#FFFFFF",  font=("Arial", font_size))
textbox_entry = tkinter.Text(frame, height=10, width=70, font=("Arial", font_size-2))

temperature_entry = tkinter.Entry(frame, font=("Arial", font_size))
temperature_entry.insert(0, "0.2")
temperature_label = tkinter.Label(
    frame, text="Temperature (0.0 - 0.9)", bg=bg_color, fg="#FFFFFF", font=("Arial", font_size))


# radio buttons
radio_button_label = tkinter.Label(
    frame, text="Select LLM Model", bg='#333333', fg="#FFFFFF",  font=("Arial", font_size))
# Variable to store the selected option
selected_model = tkinter.StringVar(value="gpt-4-1106-preview")
# Create radio buttons
radio1 = tkinter.Radiobutton(frame, text="GPT-3", variable=selected_model, bg=bg_color, fg="#FFFFFF",  value="gpt-3.5-turbo")
radio2 = tkinter.Radiobutton(frame, text="GPT-4", variable=selected_model, bg=bg_color, fg="#FFFFFF", value="gpt-4-1106-preview")


generate_button = tkinter.Button(
    frame, text="Generate", bg=bg_color, fg="#333333", font=("Arial", font_size), command=create_fetch_window)


# Placing widgets on the screen
screen_label.grid(row=0, column=0, sticky="news", pady=25)

#plcaing radio button lables
radio_button_label.grid(row=1, column=0, sticky="w")
#placing two radio buttons
radio1.grid(row=2, column=0, sticky="w")
radio2.grid(row=3, column=0, sticky="w")

#placing temperature label and entry 
temperature_label.grid(row=4, column=0, sticky="w")
temperature_entry.grid(row=5, column=0, sticky="w")

# placing text box and label
textbox_label.grid(row=6, column=0, sticky="w", pady=10)
textbox_entry.grid(row=7, column=0)

# placing generate button
generate_button.grid(row=8, column=0, columnspan=2, pady=15)

# Load the icon image 
icon_image = Image.open('./images/icon.png')
icon_photo = ImageTk.PhotoImage(icon_image)
# Set the window icon
window.iconphoto(False, icon_photo)

frame.pack()
window.mainloop()