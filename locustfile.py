from locust import User, task, between
import websockets
import asyncio

class WebSocketUser(User):
    wait_time = between(1, 2)
    
    async def connect(self):
        self.websocket = await websockets.connect("ws://echo.websocket.org")
    
    async def disconnect(self):
        await self.websocket.close()
    
    def on_start(self):
        asyncio.run(self.connect())
    
    def on_stop(self):
        asyncio.run(self.disconnect())
    
    @task
    async def send_message(self):
        try:
            await self.websocket.send("اختبار")
            response = await self.websocket.recv()
        except Exception as e:
            self.environment.events.request_failure.fire(
                request_type="WebSocket", name="send_message", response_time=0, exception=e
            )

class WebSocketLocust(User):
    abstract = True
    
    async def run(self):
        while True:
            try:
                await self.connect()
                while True:
                    await self.send_message()
                    await asyncio.sleep(self.wait_time())
            except Exception:
                await asyncio.sleep(5)
                continue
            finally:
                await self.disconnect()