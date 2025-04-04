from devices.base_device import BaseDevice
import time

start_time = time.time()

class RPMIndicator(BaseDevice):
    async def update(self, telemetry_data):

        rpm_telem = telemetry_data.get("rpm_info", {})
        if not rpm_telem:
            print("No RPM telemetry data available.")
            return

        rpm = rpm_telem.get("rpm", 0)
        shift_rpm = rpm_telem.get("shift_rpm", 0)
        blink_rpm = rpm_telem.get("blink_threshold", 0)
        first_light_rpm = rpm_telem.get("first_light_rpm", 0)
        last_light_rpm = rpm_telem.get("last_light_rpm", 0)

        gear_selection = telemetry_data.get("gear", 0)

        if gear_selection < 3:
            first_light_rpm = first_light_rpm - (blink_rpm * 0.1)

       # print(f"RPM: {rpm}, Shift RPM: {shift_rpm}, Blink RPM: {blink_rpm}, First Light RPM: {first_light_rpm}, Last Light RPM: {last_light_rpm}")

        percentage = 0
        ##if rpm is less than first_light_rpm, set to 0
        if rpm < first_light_rpm:
            percentage = 0

        if rpm >= first_light_rpm and rpm < last_light_rpm:
            percentage = (rpm - first_light_rpm) / (last_light_rpm - first_light_rpm) * 100
          
        if rpm >= blink_rpm or rpm >= shift_rpm:
            percentage = 100



       

        self.serial_handler.ser.write(f"{percentage}\n".encode())  
        try:
          self.serial_handler.ser.readline().decode().strip()  # Read response
        except Exception as e:
            print(f"Error reading response: {e}")
            response = None
        finally:
            if response:
                print(f"Response from device: {response}")
            else:
                print("No response from device.")

       
