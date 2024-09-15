# WebSocket Client Example in Backend API
import websockets
import asyncio

async def send_command_to_executor(command):
    uri = "ws://executor-server"
    async with websockets.connect(uri) as websocket:
        await websocket.send(command.serialize())  # Serialize Command object

# Usage
search_command = SearchJobCommand("LinkedIn", "Software Engineer")
asyncio.run(send_command_to_executor(search_command))