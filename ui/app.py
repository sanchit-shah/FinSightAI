import customtkinter as ctk
import tkinter as tk
from ui.sidebar import Sidebar
from ui.data_selection import DataSelectionFrame
from ui.data_preparation import DataPreparationFrame
from ui.training import TrainingFrame
from ui.evaluation import EvaluationFrame
from ui.export import ExportFrame

class MLPlatformApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ML Model Builder")
        self.root.geometry("1200x800")
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        
    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.frames = {
            'data_selection': DataSelectionFrame(self.content_area, self),
            'data_preparation': DataPreparationFrame(self.content_area),
            'training': TrainingFrame(self.content_area),
            'evaluation': EvaluationFrame(self.content_area),
            'export': ExportFrame(self.content_area)
        }
        
        self.sidebar = Sidebar(self.main_container, self)
        
        self.show_frame('data_selection')
        
    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill=tk.BOTH, expand=True)
        
    def run(self):
        self.root.mainloop()
