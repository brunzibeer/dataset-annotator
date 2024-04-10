import configparser
from src.common import SECTION_NAME, STANDARD_SECTION_NAME

class SequenceModel:
    def __init__(self, path: str, sequence_id: str = None):
        self.path = path
        self.sequence_id = sequence_id
        self.current_frame = 0
        self.standard_attributes = configparser.ConfigParser()
        self.augmented_attributes = configparser.ConfigParser()
        self.augmented_attributes.optionxform = str
        self.augmented_attributes.add_section(SECTION_NAME)

    def set_frame_path(self, frame_path: str):
        self.path = frame_path

    def set_default_attributes(self):
        # Set isIndor, cameraLow, cameraMid and cameraHigh to 0
        self.augmented_attributes.set(SECTION_NAME, "isIndoor", "0")
        self.augmented_attributes.set(SECTION_NAME, "cameraLow", "0")
        self.augmented_attributes.set(SECTION_NAME, "cameraMid", "0")
        self.augmented_attributes.set(SECTION_NAME, "cameraHigh", "0")

    def set_attribute(self, attribute_name: str, value: str):
        # Check if 'camera' is in the attribute name
        if "camera" in attribute_name:
            # If it is the case, set to 0 all other attributes with 'camera' in the name
            for key in self.augmented_attributes[SECTION_NAME]:
                if "camera" in key:
                    self.augmented_attributes.set(SECTION_NAME, key, "0")

        # If the attribute is not already set, set it
        # Else, reverse the value
        if not self.augmented_attributes.has_option(SECTION_NAME, attribute_name):
            self.augmented_attributes.set(SECTION_NAME, attribute_name, value)
        else:
            # Get the current value
            current_value = self.augmented_attributes.get(SECTION_NAME, attribute_name)
            # Reverse the value
            new_value = "0" if current_value == "1" else "1"
            # Set the new value
            self.augmented_attributes.set(SECTION_NAME, attribute_name, new_value)

    def get_attributes(self):
        return dict(self.augmented_attributes.items(SECTION_NAME))
    
    def get_std_attributes(self):
        return dict(self.standard_attributes.items(STANDARD_SECTION_NAME))
    
    def get_sequence_id(self):
        return self.sequence_id
    
    def get_current_frame(self):
        return self.current_frame
    
    def set_current_frame(self, frame: int):
        self.current_frame = frame

    def get_path(self):
        return self.path
