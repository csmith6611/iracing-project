
import tkinter as tk
import threading

class TkinterApp(threading.Thread):
    def __init__(self, device_manager, telemetry_manager):
        """Initialize the Tkinter GUI in a separate thread."""
        super().__init__()
        self.daemon = True  # Optional: dies with the main thread
        self.root = None
        self.running = True

        self.device_manager = device_manager
        self.telemetry_manager = telemetry_manager

    def run(self):
        self.root = tk.Tk()
        self.root.title("My App")

        self.label_var = tk.StringVar()
        label = tk.Label(self.root, textvariable=self.label_var)
        label.pack()

        button = tk.Button(self.root, text="Click Me", command=self.on_button_click)
        button.pack()

        self.label_var.set("Hello from thread!")

        ## Set up toggle telemetry button
        self.telemetry_button = tk.Button(self.root, text="Toggle Sample Telemetry", command=self.telemetry_manager.toggle_sample_telemetry)
        self.telemetry_button.pack(pady=10)

        ## Set up device manager button
        self.device_label = tk.Label(self.root, text="Devices: 0", font=("Arial", 14))
        self.device_label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_button_click(self):
        self.label_var.set("Button clicked!")

    def safe_update(self):
        print("Updating GUI...")
        try:
            self.label_var.set(f"updated, {len(self.device_manager.devices)} devices connected")
        except Exception as e:
            print(f"Error updating GUI: {e}")

    def on_close(self):
        self.running = False
        self.root.quit()
