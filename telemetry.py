import irsdk
import asyncio
import os
import struct



class IRacingReader:
    def __init__(self):
        ##setup variables
        self.ir = irsdk.IRSDK()
        self.data = {}
        self.sample_telem_mode = False
        self.ir_connected = False



    def scan_for_iracing_connection(self):
        if self.ir_connected and not (self.ir.is_initialized and self.ir.is_connected):
            self.ir_connected = False
            self.ir.shutdown()
            print("iRacing connection lost.")
        elif not self.ir_connected and self.ir.startup() and self.ir.is_initialized and self.ir.is_connected:
            self.ir_connected = True
            print("iRacing connection established.")

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
            self.scan_for_iracing_connection()  # Check for iRacing connection

            if self.ir_connected:
                
                self.data = {
                    "gear": self.ir['Gear'],
                    "flag": self.ir['SessionFlags'],
                    "rpm_info": {
                        "rpm": self.ir['RPM'],
                        "blink_threshold": self.ir["PlayerCarSLBlinkRPM"],
                        "first_light_rpm": self.ir["PlayerCarSLFirstRPM"],
                        "last_light_rpm": self.ir["PlayerCarSLLastRPM"],
                        "shift_rpm": self.ir["PlayerCarSLShiftRPM"],
                    }
                    # Add more variables as needed
                }
                print("r")               
            else:

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
                        
                    
                
            await asyncio.sleep(1/60)  # Run at 60Hz
