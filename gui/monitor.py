import tkinter as tk

class MonitorApp:
    def __init__(self, root, device_manager, telemetry_manager):
        self.root = root
        self.device_manager = device_manager
        self.label = tk.Label(root, text="Devices: 0", font=("Arial", 14))
        self.label.pack()
        self.telemetry_manager = telemetry_manager
        self.telemetry_button = tk.Button(root, text="Toggle Sample Telemetry", command=self.telemetry_manager.toggle_sample_telemetry)
        self.telemetry_button.pack(pady=10)


    def update(self):
        self.label.config(text=f"Devices: {len(self.device_manager.devices)}")
        self.root.after(1000, self.update)

