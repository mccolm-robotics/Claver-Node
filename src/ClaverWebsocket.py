import asyncio
import json
import websockets
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio

class ClaverWebsocket:
    def __init__(self, claverNode):
        self.claverNode = claverNode
        self.uri = "ws://localhost:6789"
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def get_loop(self):
        return self.loop

    async def __authenticate_connection(self, websocket: websockets) -> bool:
        credentials = json.dumps({"agent": 'browser', "bid": 'cb6070bf-e9aa-11ea-97ab-7085c2d6de42', "token": '958058', "mode": 'WhiteBoard'})
        await websocket.send(credentials)
        response = await websocket.recv()
        data = json.loads(response)
        GLib.idle_add(self.claverNode.update_gui, data)
        return True

    async def send_data(self, data):
        message = json.dumps(data)
        await self.websocket.send(message)

    async def __run(self):
        authenticated = False
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            while True:
                try:
                    if not authenticated:
                        authenticated = await self.__authenticate_connection(websocket)
                    else:
                        message = await websocket.recv()
                        data = json.loads(message)
                        GLib.idle_add(self.claverNode.update_gui, data)
                except websockets.ConnectionClosed:
                    break

    def run_asyncio(self):
        try:
            self.loop.run_until_complete(self.__run())
        except KeyboardInterrupt:
            pass
        except ConnectionRefusedError:
            print("Connection refused. Server offline")