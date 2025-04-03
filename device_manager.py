import asyncio
import os
import serial
import serial.tools.list_ports
import time
from devices.flag_indicator import FlagIndicator
from devices.rpm_indicator import RPMIndicator
from serial_handler import SerialHandler


SUPPORTED_DEVICES = ["RPMIndicator", "FlagIndicator"]  # Add other supported devices here


class DeviceManager:
    def __init__(self):
        self.devices = {}

    async def update_devices(self, telemetry_data):
        """Updates all registered devices asynchronously."""
        tasks = []
        for device in self.devices.values():
            tasks.append(device['device_handler'].update(telemetry_data))

        if tasks:
            await asyncio.gather(*tasks)
    
    async def scan_devices(self):
        """Scans for devices (placeholder for future implementation)."""
        print("[INFO] Scanning for devices...")
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device not in self.devices:
                print(f"[INFO] Found device: {port.device}")
                # Placeholder for device connection logic
                try:
                    ser = serial.Serial(port.device, 9600, timeout=1)
                    time.sleep(2)  # Allow time for device to initialize
                    ser.write(b"IDENTIFY\n")
                    response = ser.readline().decode("utf-8", errors="ignore").strip()
                    if response.startswith("vCAN.ECU:"):
                        print(f"[INFO] Device identified: {response}")
                        device_type = response.split(":")[1]

                        if device_type not in SUPPORTED_DEVICES:
                            print(f"[ERROR] Unsupported device type: {device_type}")
                            continue
                        
                        # Here you would create the device handler instance
                        # For example:
                        device_handler = None
                        serial_handler = SerialHandler(ser)
                        if device_type == "RPMIndicator":
                            device_handler = RPMIndicator(serial_handler=serial_handler)
                        if device_type == "FlagIndicator":
                            device_handler = FlagIndicator(serial_handler=serial_handler)

                        if not device_handler:
                            print(f"[ERROR] Failed to create device handler for {device_type}")
                            continue 

                        self.devices[port.device] = {"type": device_type, "device_handler": device_handler }
                        
                        print(f"[INFO] Device added: {device_type} on {port.device}")
                except Exception as e:
                    print(f"[ERROR] Failed to connect to device on {port.device}: {e}")