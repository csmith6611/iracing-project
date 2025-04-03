import tkinter as tk
import threading
import time
import struct
import os

data_file = "telemetry.ibt"
running = False

# Simulated car parameters
rpm = 0.0
throttle = 0.0
brake = 0.0
direction = 1  # 1 for accelerating, -1 for decelerating

# Constants
RPM_MAX = 7000
ACCEL_RATE = 500
DECEL_RATE = 700
TICK_RATE = 1 / 30

def write_telemetry():
    global rpm, throttle, brake, running, direction
    with open(data_file, "wb") as f:
        while running:
            if direction == 1:
                throttle = min(1.0, throttle + 0.02)
                brake = 0.0
                rpm += ACCEL_RATE
                if rpm >= RPM_MAX:
                    direction = -1
            else:
                throttle = max(0.0, throttle - 0.02)
                brake = min(1.0, brake + 0.02)
                rpm -= DECEL_RATE
                if rpm <= 0:
                    rpm = 0
                    direction = 1

            # Pack data in binary format (float values)
            data = struct.pack("fff", brake, throttle, rpm)
            f.write(data)
            f.flush()
            
            update_display()
    #close file
    f.close()
    time.sleep(TICK_RATE)

def start_simulation():
    global running
    if not running:
        running = True
        threading.Thread(target=write_telemetry, daemon=True).start()

def stop_simulation():
    global running
    running = False

def update_display():
    rpm_label.config(text=f"RPM: {int(rpm)}")
    throttle_label.config(text=f"Throttle: {throttle:.2f}")
    brake_label.config(text=f"Brake: {brake:.2f}")

# GUI Setup
root = tk.Tk()
root.title("iRacing Telemetry Simulator")

rpm_label = tk.Label(root, text="RPM: 0", font=("Arial", 16))
rpm_label.pack()

throttle_label = tk.Label(root, text="Throttle: 0.00", font=("Arial", 16))
throttle_label.pack()

brake_label = tk.Label(root, text="Brake: 0.00", font=("Arial", 16))
brake_label.pack()

start_button = tk.Button(root, text="Start", command=start_simulation)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_simulation)
stop_button.pack()

root.mainloop()
