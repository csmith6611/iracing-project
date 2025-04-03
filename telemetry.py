import irsdk
import asyncio
import os
import struct



class IRacingReader:
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.ir.startup()
        self.data = {}
        self.iracing_running = False
        self.sample_telem_mode = False

    def read_sample_telemetry(self):
        if not os.path.exists("telemetry.ibt"):
            print("Telemetry file not found.")
            return None
        with open("telemetry.ibt", "rb") as f:
            data = f.read(12)
            return data
    
    def toggle_sample_telemetry(self):
        self.sample_telem_mode = not self.sample_telem_mode
        if self.sample_telem_mode:
            print("Sample telemetry mode enabled.")
        else:
            print("Sample telemetry mode disabled.")

    async def update(self):
        while True:
            if self.ir.is_connected and self.ir.is_running:
                self.iracing_running = True
                self.data = {
                    "flag": self.ir['SessionFlags'],
                    "rpm": self.ir['RPM'],
                    # Add more variables as needed
                }
                print(f"Telemetry Data: {self.data}")
            else:
                self.iracing_connected = False

                if self.sample_telem_mode:
                    try: 
                        data = self.read_sample_telemetry()
                        brake, throttle, rpm = struct.unpack("fff", data)
                        print(f"Sample Telemetry Data: Brake: {brake}, Throttle: {throttle}, RPM: {rpm}")
                        self.data = {
                            "flag": 0,  # Placeholder for session flags
                            "rpm": rpm,
                            "brake": brake,
                            "throttle": throttle,
                        }
                    except Exception as e:
                        print(f"Error reading sample telemetry: {e}")
                        
                    
                else:
                    print("iRacing is not connected or not running.")
            await asyncio.sleep(1)  # Run at 60Hz
