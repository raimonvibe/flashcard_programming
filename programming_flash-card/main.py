# Importing necessary libraries
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Reading data from CSV file
try:
    data = pandas.read_csv("data/terms_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/programming_terms.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# Function to display the next flashcard
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Term", fill="black")
    canvas.itemconfig(card_word, text=current_card["Term"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

# Function to flip the flashcard and display the meaning
def flip_card():
    canvas.itemconfig(card_title, text="Meaning", fill="white")
    meaning_text = current_card["Meaning"]
    formatted_text = ""
    words = meaning_text.split(" ")
    for i, word in enumerate(words):
        formatted_text += word
        if (i + 1) % 4 == 0:  # Add newline after every 4 words
            formatted_text += "\n"
        else:
            formatted_text += " "
    canvas.itemconfig(card_word, text=formatted_text, fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# Function to handle known flashcards
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/terms_to_learn.csv", index=False)
    next_card()

# Creating the main window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Setting up the flip timer
flip_timer = window.after(3000, func=flip_card)

# Creating the canvas for displaying flashcards
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 120, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 320, text="", font=("Arial", 40, "bold"), width=600, justify=CENTER)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Creating buttons for known and unknown flashcards
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# Displaying the first flashcard
next_card()

# Running the main event loop
window.mainloop()
