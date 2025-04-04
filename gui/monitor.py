
import tkinter as tk
import threading
from tkinter import ttk

class TkinterApp(threading.Thread):
    def __init__(self, device_manager, telemetry_manager):
        """Initialize the Tkinter GUI in a separate thread."""
        super().__init__()
        self.daemon = True  # Optional: dies with the main thread
        self.root = None
        self.running = True

        self.device_manager = device_manager
        self.telemetry_manager = telemetry_manager

        self.current_page = None

    def run(self):
        self.root = tk.Tk()
        self.root.title("Device Manager")
        self.root.geometry("600x400")
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")


        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)


        self.frames = {}

        for F in (MainPage, ConfigPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()
        self.current_page = page_name
    
    def toggle_overlay(self, show=True):
        """Toggle the simulator overlay on the main page."""
        main_page = self.frames["MainPage"]
        main_page.set_simulator_overlay(show)

    def safe_update(self):
        print("Updating GUI...")
        try:
            if self.current_page == "MainPage":
                main_page = self.frames["MainPage"]
                main_page.update(self.device_manager, self.telemetry_manager)

        except Exception as e:
            print(f"Error updating GUI: {e}")

    def on_close(self):
        self.running = False
        self.root.quit()




class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header
        ttk.Label(self, text="Connected Devices", font=("Helvetica", 18)).pack(pady=10)

        # Device count label
        self.device_count_label = ttk.Label(self, text="Devices connected: 0", font=("Helvetica", 14))
        self.device_count_label.pack(pady=5)

        # Device list frame
        self.device_list_frame = ttk.Frame(self)
        self.device_list_frame.pack(fill="x", padx=20, pady=10)

        # Configuration button
        ttk.Button(self, text="Go to Configuration", command=lambda: controller.show_frame("ConfigPage")).pack(pady=20)

        # Simulator overlay (initially hidden)
        # self.overlay = tk.Label(self, text="SIMULATOR RUNNING", bg="black", fg="white", font=("Helvetica", 20), padx=20, pady=10)
        # self.overlay.place(relx=0.5, rely=0.1, anchor="n")
        # self.overlay.lower()
    
    def update(self, device_manager, telemetry_manager):
        """Update the device list and telemetry data."""
        # Update device count label
        device_count = len(device_manager.devices)
        self.device_count_label.config(text=f"Devices connected: {device_count}")

        # Update device list (placeholder for actual device details)
        for widget in self.device_list_frame.winfo_children():
            widget.destroy()
        
        for device in device_manager.devices.values():
            device_label = ttk.Label(self.device_list_frame, text=f"Device: {device['type']}", anchor="w")
            device_label.pack(fill="x", pady=2)

    def set_simulator_overlay(self, show=True):
        if show:
            self.overlay.lift()
        else:
            self.overlay.lower()

class ConfigPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Device Configuration", font=("Helvetica", 18)).pack(pady=10)

        # Device selection
        ttk.Label(self, text="Select Device").pack(pady=5)
        self.device_select = ttk.Combobox(self, values=["Device 1", "Device 2"])
        self.device_select.pack(pady=5)

        # Mode selection
        ttk.Label(self, text="Select Mode").pack(pady=5)
        self.mode_select = ttk.Combobox(self, values=["Monitor", "Config", "Sleep"])
        self.mode_select.pack(pady=5)

        # Back button
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("MainPage")).pack(pady=20)
