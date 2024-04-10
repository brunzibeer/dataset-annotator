from tkinter import Tk, Frame, Label, Button, Entry
from PIL import ImageTk, Image
from src.models.sequence import SequenceModel

class MainWindow():
    def __init__(self, master: Tk):
        self.master = master
        self.master.title("Image Labeling App")

        self.current_image_index = 0

        # Frame to display the image
        self.image_frame = Frame(self.master)
        self.image_frame.pack(side="left")

        self.image_label = Label(self.image_frame)
        self.image_label.pack()

        # Frame to hold attribute buttons
        self.attribute_buttons_frame = Frame(self.master)
        self.attribute_buttons_frame.pack(side="right")

        # Frame to be placed right to the image and top to the buttons
        self.standard_attributes_frame = Frame(self.master)
        self.standard_attributes_frame.pack(side="right", anchor="n")

    def display_image(self, image: SequenceModel):
        image_path = image.get_path()
        img = Image.open(image_path)
        img = img.resize((1280, 720), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)
    
    def add_prev_button(self):
        button = Button(self.image_frame, text="Prev")
        button.pack(side="left")
    
    def add_next_button(self):
        button = Button(self.image_frame, text="Next")
        button.pack(side="right")

    def add_search_entry(self):
        entry = Entry(self.image_frame)
        entry.pack(side="bottom")

        return entry

    def add_other_frame_button(self):
        button = Button(self.attribute_buttons_frame, text="Next Frame (Space)")
        button.pack(side="top", pady=20)

    def add_attribute_button(self, text):
        button = Button(self.attribute_buttons_frame, text=text)
        button.pack(side="top")

        return button
    
    def add_standard_attributes_label(self, text):
        label = Label(self.standard_attributes_frame, text=text)
        label.pack(side="top")

        return label
    
    def change_button_color(self, button: Button, color: str):
        button.config(fg=color)

    def change_label_text(self, label: Label, text: str):
        label.config(text=text)
