import asyncio
import serial
import serial_asyncio
import os



class SerialHandler:
    def __init__(self, ser):
        self.ser = ser
        self.queue = asyncio.Queue()

    async def _serial_writer_task(self):
        """Continuously sends messages from the queue to the serial port."""
        print("Serial writer task started.")
        while True:
            message = await self.queue.get()
            print(f"Sending message: {message}")
            self.ser.write(message.encode() + b'\n')
            await self.queue.task_done()

    async def send(self, message):
        """Queues a message for transmission."""
        await self.queue.put(message)


# Example usage:
# serial_handler = SerialHandler(port="COM3", frontend_development=True)
# asyncio.run(serial_handler.connect())
# asyncio.run(serial_handler.send("Hello ESP32"))
