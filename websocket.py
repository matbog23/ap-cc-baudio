import asyncio
import websockets

async def send_result(websocket, path):
    # Perform OpenAI API request and get result
    result = "Your OpenAI API result here"

    # Send the result over the WebSocket connection
    await websocket.send(result)

start_server = websockets.serve(send_result, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
