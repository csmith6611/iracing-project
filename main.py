import asyncio
import tkinter as tk
from telemetry import IRacingReader
from device_manager import DeviceManager
from gui.monitor import TkinterApp

async def async_tasks(telemetry, device_manager, gui_callback):
    """Runs telemetry updates and device updates in an async loop."""
    telemetry_task = asyncio.create_task(telemetry.update())  # Get latest iRacing data
    gui_task = asyncio.create_task(update_gui(gui_callback, telemetry))  # Update GUI asynchronously


    while True:
        if not telemetry.ir_connected and not telemetry.sample_telem_mode:
            await device_manager.scan_devices()  # Scan for devices if iRacing is not running
            await asyncio.sleep(1)
        else:
            await device_manager.update_devices(telemetry.data)  # Send updates to ESP32s
            await asyncio.sleep(1/60)  # Maintain 60Hz refresh rate

async def update_gui(callback, telemetry):
    while True:
        if telemetry.ir_connected:
           callback()
           await asyncio.sleep(10)
        # Call the callback function to update the GUI
        else: 
            callback()
            await asyncio.sleep(1)

def main():
    #initialize sample telemetry mode

    # Initialize components
    telemetry = IRacingReader()
    device_manager = DeviceManager()

    # Register devices
    print("[INFO] Registering devices...")
    


    # Initialize GUI
    app = TkinterApp(device_manager=device_manager, telemetry_manager=telemetry)
    app.start()  # Start the Tkinter GUI in a separate thread


    # Run async tasks (telemetry + device updates)
    asyncio.run(async_tasks(telemetry, device_manager, gui_callback=app.safe_update))



if __name__ == "__main__":
    main()
