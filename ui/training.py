import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import queue
import time

class TrainingFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.is_training = False
        self.training_thread = None
        self.data_queue = queue.Queue()
        self.training_data = {
            'loss': [], 'accuracy': [],
            'val_loss': [], 'val_accuracy': []
        }
        self.setup_frame()
        self.setup_plot()
        
    def setup_frame(self):
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(pady=10)
        
        self.train_button = ctk.CTkButton(
            controls_frame,
            text="Start Training",
            command=self.toggle_training
        )
        self.train_button.pack(side=tk.LEFT, padx=5)
        
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Navigation frame at the bottom
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Back to Data Preparation",
            command=lambda: self.app.show_frame('data_preparation')
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next: Evaluate Results →",
            command=lambda: self.app.show_frame('evaluation')
        )
        self.next_button.pack(side=tk.RIGHT)
        
    def setup_plot(self):
        self.fig, self.ax1 = plt.subplots(figsize=(6, 4))
        self.ax2 = self.ax1.twinx()
        
        self.ax1.set_xlabel('Epoch')
        self.ax1.set_ylabel('Loss', color='tab:blue')
        self.ax2.set_ylabel('Accuracy', color='tab:orange')
        self.fig.suptitle('Training Progress')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.loss_line, = self.ax1.plot([], [], 'b-', label='Training Loss')
        self.val_loss_line, = self.ax1.plot([], [], 'b--', label='Validation Loss')
        self.acc_line, = self.ax2.plot([], [], 'orange', label='Training Accuracy')
        self.val_acc_line, = self.ax2.plot([], [], 'orange', linestyle='--', label='Validation Accuracy')
        
        self.ax1.tick_params(axis='y', labelcolor='tab:blue')
        self.ax2.tick_params(axis='y', labelcolor='tab:orange')
        
        lines1, labels1 = self.ax1.get_legend_handles_labels()
        lines2, labels2 = self.ax2.get_legend_handles_labels()
        self.ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        self.fig.tight_layout()
        
    def toggle_training(self):
        if not self.is_training:
            self.start_training()
        else:
            self.stop_training()
            
    def start_training(self):
        self.is_training = True
        self.train_button.configure(text="Stop Training")
        self.training_thread = threading.Thread(target=self.training_loop)
        self.training_thread.start()
        self.update_plot()
        
    def stop_training(self):
        self.is_training = False
        self.train_button.configure(text="Start Training")
        if self.training_thread:
            self.training_thread.join()
    
    #simulating a training loop, change this to call a function that does the actual training
    def training_loop(self):
        epoch = 0
        while self.is_training and epoch < 100:
            loss = np.exp(-epoch/30) + np.random.normal(0, 0.1)
            val_loss = loss + np.random.normal(0, 0.1)
            accuracy = 1 - np.exp(-epoch/30) + np.random.normal(0, 0.1)
            val_accuracy = accuracy + np.random.normal(0, 0.1)
            
            self.data_queue.put({
                'loss': loss,
                'val_loss': val_loss,
                'accuracy': accuracy,
                'val_accuracy': val_accuracy
            })
            
            epoch += 1
            time.sleep(0.1)
            
    def update_plot(self):
        if self.is_training:
            while not self.data_queue.empty():
                data = self.data_queue.get()
                for key, value in data.items():
                    self.training_data[key].append(value)
                    
            x = list(range(len(self.training_data['loss'])))
            self.loss_line.set_data(x, self.training_data['loss'])
            self.val_loss_line.set_data(x, self.training_data['val_loss'])
            self.acc_line.set_data(x, self.training_data['accuracy'])
            self.val_acc_line.set_data(x, self.training_data['val_accuracy'])
            
            self.ax1.relim()
            self.ax2.relim()
            self.ax1.autoscale_view()
            self.ax2.autoscale_view()
            
            self.canvas.draw()
            
            self.after(100, self.update_plot)
