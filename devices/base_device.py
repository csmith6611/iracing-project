import os


class BaseDevice:
    def __init__(self, serial_handler):
        self.serial_handler = serial_handler

    async def update(self, telemetry_data):
        """Subclasses must implement this."""
        raise NotImplementedError

