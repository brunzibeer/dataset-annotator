import argparse
from tkinter import Tk
from src.views.main_window import MainWindow
from src.controllers.sequence_loader import SequenceController

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Image Labeling App")
    parser.add_argument("--sq_path", help="Path to the sequences folder")
    parser.add_argument("--frames_path", help="Path to the frames folder")
    args = parser.parse_args()

    root = Tk()
    app = MainWindow(root)
    sequence_controller = SequenceController(app, args.sq_path, args.frames_path)
    root.mainloop()

if __name__ == "__main__":
    main()
