import os


class BaseDevice:
    def __init__(self, serial_handler):
        self.serial_handler = serial_handler

    async def update(self, telemetry_data):
        """Subclasses must implement this."""
        raise NotImplementedError

    async def ping(self):
        """Ping the device to check if it's responsive."""
        try:
            self.serial_handler.ser.write(b"PING\n")
            response = self.serial_handler.ser.readline().decode("utf-8", errors="ignore").strip()
            if response == "PONG":
               return True
            else:
                return False
        except Exception as e:
            print(f"[ERROR] Failed to ping device: {e}")
            return False