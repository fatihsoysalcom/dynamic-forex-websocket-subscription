import asyncio
import websockets
import json

# Replace with your actual WebSocket API endpoint
# This is a placeholder and may not be a real Forex WebSocket API
WEBSOCKET_URL = "wss://fxtrading.example.com/ws"

async def subscribe_to_pairs(websocket, pairs):
    """Sends subscription messages for the given Forex pairs."""
    for pair in pairs:
        # Example subscription message format. This will vary by API.
        subscribe_message = {
            "action": "subscribe",
            "symbol": pair
        }
        await websocket.send(json.dumps(subscribe_message))
        print(f"Subscribed to: {pair}")

async def unsubscribe_from_pairs(websocket, pairs):
    """Sends unsubscription messages for the given Forex pairs."""
    for pair in pairs:
        # Example unsubscription message format. This will vary by API.
        unsubscribe_message = {
            "action": "unsubscribe",
            "symbol": pair
        }
        await websocket.send(json.dumps(unsubscribe_message))
        print(f"Unsubscribed from: {pair}")

async def receive_data(websocket):
    """Receives and processes data from the WebSocket."""
    try:
        async for message in websocket:
            # Process the received data (e.g., print it)
            print(f"Received: {message}")
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed gracefully.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    # Initially, subscribe to a few pairs
    initial_pairs = ["EURUSD", "GBPUSD"]
    # Pairs to dynamically add later
    new_pairs = ["USDJPY", "AUDUSD"]
    # Pairs to dynamically remove later
    pairs_to_remove = ["EURUSD"]

    async with websockets.connect(WEBSOCKET_URL) as websocket:
        print("Connected to WebSocket.")

        # Dynamically subscribe to initial pairs
        await subscribe_to_pairs(websocket, initial_pairs)

        # Start receiving data in the background
        receiver_task = asyncio.create_task(receive_data(websocket))

        # Simulate a delay before dynamic changes
        await asyncio.sleep(5)

        # Dynamically subscribe to new pairs
        await subscribe_to_pairs(websocket, new_pairs)

        # Simulate another delay
        await asyncio.sleep(5)

        # Dynamically unsubscribe from some pairs
        await unsubscribe_from_pairs(websocket, pairs_to_remove)

        # Keep the connection open for a bit longer to see remaining data
        await asyncio.sleep(10)

        # Cleanly close the connection (optional, as context manager does it)
        # await websocket.close()
        await receiver_task # Ensure receiver task finishes

if __name__ == "__main__":
    # Note: This example uses a placeholder URL. You'll need a real Forex WebSocket API.
    # Running this will attempt to connect and send/receive messages based on the example logic.
    # Ensure you have a running WebSocket server that understands these message formats for actual testing.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user.")
