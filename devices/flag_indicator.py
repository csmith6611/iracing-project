from devices.base_device import BaseDevice

class FlagIndicator(BaseDevice):
    async def update(self, telemetry_data):
        flag = telemetry_data.get("flag", 0)
        color = "OFF"
        if flag & 0x1:  # Green flag
            color = "GREEN"
        elif flag & 0x2:  # Yellow flag
            color = "YELLOW"

        await self.serial_handler.send(f"FLAG {color}\n")  

