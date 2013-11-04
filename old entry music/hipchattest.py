from hipchat import HipChat

ROOM_ID = 90507
HIPCHAT_API_TOKEN = 'a864d83d6221ad09861b690109a9f7'

hipster = HipChat(token=HIPCHAT_API_TOKEN)

hipster.method('rooms/message', method='POST', parameters={'room_id': ROOM_ID, 'from': 'The Announcer', 'message': 'All your base...'})
