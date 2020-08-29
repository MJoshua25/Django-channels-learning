import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


class ChatChonsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print("connected", event)

		other_user = self.scope['url_route']['kwargs']['username']
		me = self.scope['user']
		# print(me, other_user)
		thread_obj = await self.get_thread(me, other_user)
		chat_room = "thread_{}".format(thread_obj.id)
		self.chat_room = chat_room
		await self.channel_layer.group_add(
			chat_room,
			self.channel_name
		)
		await self.send({
			'type': "websocket.accept"
		})

	# print(thread_obj)

	# await asyncio.sleep(10)

	async def websocket_receive(self, event):
		print("received", event)
		front_text = event.get('text', None)
		if front_text is not None:
			loaded_dict_data = json.loads(front_text)
			msg = loaded_dict_data.get('message')
			print(msg)
			user = self.scope['user']
			username = 'default'
			if user.is_authenticated:
				username = user.username
			myResponse = {
				'message': msg,
				'username': username
			}
			new_event = {
				'type': "websocket.send",
				'text': json.dumps(myResponse)
			}
			await self.channel_layer.groupe_send(
				self.chat_room,
				new_event
			)

	async def websocket_disconnect(self, event):
		print("disconnected", event)

	@database_sync_to_async
	def get_thread(self, user, other_username):
		return Thread.objects.get_or_new(user, other_username)[0]
