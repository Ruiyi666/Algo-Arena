from django.core.cache import cache

from channels.generic.websocket import (
    AsyncWebsocketConsumer,
    WebsocketConsumer,
    JsonWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)

# a simple lock step game, 4 frames per second
# 1. client sends action to server
# 2. server receives action and stores it in cache
# 3. server sends action to all clients when the frame is reached


class PlayerActionConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "interactions_%s" % self.room_name

        if not cache.has_key(self.room_group_name):
            cache.set(self.room_group_name, True)
            cache.set(f"{self.room_group_name}-connections", 0)
            cache.set(f"{self.room_group_name}-action_frame", [])

        self.player = cache.get(f"{self.room_group_name}-connections")
        cache.incr(f"{self.room_group_name}-connections")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print("PlayerActionConsumer: connect: room_group_name: ", self.room_group_name)
        await self.accept()

    async def disconnect(self, close_code):
        print(
            "PlayerActionConsumer: disconnect: room_group_name: ", self.room_group_name
        )

        cache.decr(f"{self.room_group_name}-connections")
        if cache.get(f"{self.room_group_name}-connections") == 0:
            cache.delete(self.room_group_name)
            cache.delete(f"{self.room_group_name}-connections")
            cache.delete(f"{self.room_group_name}-action_frame")
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        pass

    # Receive message from WebSocket
    async def receive_json(self, content):
        # print("content: ", content)
        # store the action in cache
        action_frame = cache.get(f"{self.room_group_name}-action_frame")

        content = [
            {
                "player": self.player,
                "operation": action["operation"],
            }
            for action in content
        ]

        action_frame.extend(content)

        cache.set(f"{self.room_group_name}-action_frame", action_frame)
        # and wait for the frame to be reached
        # the frame is the number of frames per second
        # there should be 2 users in the room
        if cache.get(f"{self.room_group_name}-connections") == len(
            cache.get(f"{self.room_group_name}-action_frame")
        ):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "player_action",
                    "message": cache.get(f"{self.room_group_name}-action_frame"),
                },
            )
            # reset the frame
            cache.set(f"{self.room_group_name}-action_frame", [])
        # reset the number of connections

    # Receive message from room group
    async def player_action(self, event):
        message = event["message"]
        if self.player == 1:
            message = [
                {
                    "player": 1 - action["player"],
                    "operation": action["operation"],
                }
                for action in message
            ]
        print("PlayerActionConsumer: player_action: message: ", message)
        # Send message to WebSocket
        await self.send_json(message)
