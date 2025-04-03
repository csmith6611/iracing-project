from devices.base_device import BaseDevice

class RPMIndicator(BaseDevice):
    async def update(self, telemetry_data):
        rpm = telemetry_data.get("rpm", 0)
        percentage = rpm / 7000 * 100 # Assuming 7000 is the max RPM
        percentage = max(1, min(100, percentage))  # Clamp between
        percentage = round(percentage, 2)
        self.serial_handler.ser.write(f"{percentage}\n".encode())  
        
        try:
            response = self.serial_handler.ser.readline().decode().strip()  # Read response
        except Exception as e:
            print(f"Error reading response: {e}")
            response = None
        if response:
            print(f"Received: {response}")
