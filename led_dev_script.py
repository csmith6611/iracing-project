import serial
import time
import math



def get_smooth_percentage(t, period=2):
    return (math.sin(2 * math.pi * t / period) + 1) * 50

start_time = time.time()



# Set up serial connection (adjust port as necessary)
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Allow time for Arduino to initialize

try:
    while True:
        elapsed_time = time.time() - start_time
        percentage = get_smooth_percentage(elapsed_time)
        percentage = max(1, min(100, percentage))  # Clamp between
        percentage = round(percentage, 2)
        ser.write(f"{percentage}\n".encode())  # Send as string
        print(f"Sent: {percentage}")
        try:
            response = ser.readline().decode().strip()  # Read response
        except Exception as e:
            print(f"Error reading response: {e}")
            response = None
        if response:
            print(f"Received: {response}")
        
        time.sleep(1 / 60)  # Small delay
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()