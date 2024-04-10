# image_controller.py
import os
from typing import List
import random

from src.views.main_window import MainWindow
from src.models.sequence import SequenceModel
from src.common import AGUMENTED_ATTRIBUTES_FILE, HIGHLIGHT_COLOR, NORMAL_COLOR

class SequenceController:
    def __init__(self, view: MainWindow, sq_path: str = None, frames_path: str = None):
        self.view = view
        self.images: List[SequenceModel] = []
        self.labels = {}
        self.buttons = {}
        self.sq_path = sq_path
        self.frames_path = frames_path
        self.current_sequence_index = 0

        self.display_labels()
        self.load_sequences()
        self.display_buttons()
        self.display_search_entry()

    def load_sequences(self):
        sequences = sorted(os.listdir(self.sq_path))
        
        for sequence in sequences:
            image_path = os.path.join(self.frames_path, sequence, 'rgb', '0000.jpg')
            sequence_model = SequenceModel(image_path, sequence)
            self.images.append(sequence_model)

            # Load standard attributes
            standard_info = os.path.join(self.sq_path, sequence, 'seqinfo.ini')
            assert os.path.exists(standard_info), f"seqinfo.ini file not found for sequence {sequence}"
            sequence_model.standard_attributes.read(standard_info)

            # Check if the 'aug-info.ini' file exists
            aug_info = os.path.join(self.sq_path, sequence, AGUMENTED_ATTRIBUTES_FILE)
            if os.path.exists(aug_info):
                sequence_model.augmented_attributes.read(aug_info)
            else:
                sequence_model.set_default_attributes()

        self.view.display_image(self.images[self.current_sequence_index])
        self.change_label_text()

    def display_buttons(self):
        attributes = (
            ("Indoor (I)", "i", "isIndoor=1"),
            ("Low Camera (1)", "1", "cameraLow=1"),
            ("Mid Camera (2)", "2", "cameraMid=1"),
            ("High Camera (3)", "3", "cameraHigh=1")
        )

        for attribute, binding, value in attributes:
            btn = self.view.add_attribute_button(attribute)
            option, _ = value.split("=")
            self.buttons[option] = btn

            self.view.master.bind(binding, lambda e, value=value: self.apply_attribute(value))

        self.view.add_other_frame_button()
        self.view.master.bind("<space>", lambda e: self.another_frame())

        self.view.add_prev_button()
        self.view.master.bind("<Left>", lambda e: self.prev_image())
        self.view.add_next_button()
        self.view.master.bind("<Right>", lambda e: self.next_image())

        self.color_buttons()

    def display_labels(self):
        labels = (
            ('', 'moving'),
            ('', 'night'),
            ('', 'weather')
        )

        for label, idx in labels:
            self.labels[idx] = self.view.add_standard_attributes_label(label)

    def display_search_entry(self):
        entry = self.view.add_search_entry()
        entry.bind("<Return>", lambda e: self.search_sequence(entry.get()))

    def search_sequence(self, sequence_id: str):
        # Check if the sequence id is valid, it has to be between 0 and the number of sequences
        int_sequence_id = int(sequence_id)
        if int_sequence_id < 0 or int_sequence_id >= len(self.images) or not sequence_id.isdigit():
            return
        else:
            sequence_id = sequence_id.strip().zfill(3)
        # Search for the sequence with the given id
        sequence = next((s for s in self.images if s.get_sequence_id() == sequence_id), None)

        if sequence:
            print(f"Current sequence index: {self.current_sequence_index}")
            self.current_sequence_index = self.images.index(sequence)
            print(f"Current sequence index: {self.current_sequence_index}")
            self.view.display_image(sequence)
            self.change_label_text()
            self.color_buttons()
            self.view.master.focus()


    def prev_image(self):
        self.save_attributes()

        if self.current_sequence_index > 0:
            self.current_sequence_index -= 1
            self.view.display_image(self.images[self.current_sequence_index])

        self.color_buttons()
        self.change_label_text()

    def next_image(self):
        self.save_attributes()

        if self.current_sequence_index < len(self.images) - 1:
            self.current_sequence_index += 1
            self.view.display_image(self.images[self.current_sequence_index])

        self.color_buttons()
        self.change_label_text()
    
    def another_frame(self):
        sequence = self.images[self.current_sequence_index]
        current_frame = sequence.get_current_frame()
        frame_string = str(current_frame + 10).zfill(4) + ".jpg" if current_frame < 1798 else str(0).zfill(4) + ".jpg"
        sequence.set_frame_path(os.path.join(self.frames_path, sequence.get_sequence_id(), 'rgb', frame_string))

        sequence.set_current_frame(current_frame + 10 if current_frame < 1798 else 0)

        # Display the new image
        self.view.display_image(sequence)

    def apply_attribute(self, value: str):
        option, value = value.split("=")
        self.images[self.current_sequence_index].set_attribute(option, value)

        self.save_attributes()
        self.color_buttons()

    def save_attributes(self):
        sequence: SequenceModel = self.images[self.current_sequence_index]
        aug_info = os.path.join(self.sq_path, sequence.get_sequence_id(), AGUMENTED_ATTRIBUTES_FILE)

        with open(aug_info, "w") as file:
            sequence.augmented_attributes.write(file)

    def color_buttons(self):
        # When an attribute button gets pressed, it should change color based on the attributes
        # Retrieve the attributes from the current image
        current_image = self.images[self.current_sequence_index]
        attributes = current_image.get_attributes()

        # For each button, if the attribute is set, change the color
        for att in attributes:
            if attributes[att] == "1":
                self.view.change_button_color(self.buttons[att], HIGHLIGHT_COLOR)
            else:
                self.view.change_button_color(self.buttons[att], NORMAL_COLOR)

    def change_label_text(self):
        sequence = self.images[self.current_sequence_index]
        # Get standard attributes
        standard_attributes = sequence.get_std_attributes()

        for k in self.labels.keys():
            for att in standard_attributes:
                if k in att:
                    text = f"{att} = {standard_attributes[att]}"
                    self.view.change_label_text(self.labels[k], text)
