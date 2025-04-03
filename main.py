import asyncio
import threading
import tkinter as tk
from telemetry import IRacingReader
from device_manager import DeviceManager


from gui.monitor import MonitorApp

async def async_tasks(telemetry, device_manager):
    """Runs telemetry updates and device updates in an async loop."""
    telemetry_task = asyncio.create_task(telemetry.update())  # Get latest iRacing data

    while True:
        if not telemetry.iracing_running and not telemetry.sample_telem_mode:
            await device_manager.scan_devices()  # Scan for devices if iRacing is not running
            await asyncio.sleep(1)
        else:
            await device_manager.update_devices(telemetry.data)  # Send updates to ESP32s
            await asyncio.sleep(1/60)  # Maintain 60Hz refresh rate

def start_tkinter_gui(device_manager, telemetry):
    """Starts the Tkinter GUI in the main thread."""
    root = tk.Tk()
    gui = MonitorApp(root, device_manager, telemetry_manager=telemetry)
    root.mainloop()


def main():
    #initialize sample telemetry mode

    # Initialize components
    telemetry = IRacingReader()
    device_manager = DeviceManager()

    # Register devices
    print("[INFO] Registering devices...")
    


    # Start Tkinter GUI in the main thread
    tk_thread = threading.Thread(target=start_tkinter_gui, args=(device_manager, telemetry), daemon=True)
    tk_thread.start()

    # Run async tasks (telemetry + device updates)
    asyncio.run(async_tasks(telemetry, device_manager))

if __name__ == "__main__":
    main()
