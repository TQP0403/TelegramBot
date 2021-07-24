import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest, AddChatUserRequest
from telethon.tl.types import InputPeerEmpty, PeerChannel, PeerChat, Chat, Channel, InputPeerChannel, InputPeerChat
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import UserAlreadyParticipantError, ChatAdminRequiredError, UserPrivacyRestrictedError, PeerFloodError

load_dotenv()

API_ID = os.getenv('API_ID1')
API_HASH = os.getenv('API_HASH1')
USER_NAME = os.getenv('USER_NAME1') #login as a bot
PHONE = os.getenv('PHONE1') #login as a user

client = TelegramClient(PHONE, API_ID, API_HASH)
print('Telegram client start')

client.connect()

channel_groups = []
chat_groups = []

# target_id: int = 1364412069 # PegaSwap
target_id: int = 1222311777 # DeFi Space

src_ids = [
    1364412069, # CoinMarketCap Announcements
    1381405351, # CoinMarketCap English
]

result = client(GetDialogsRequest(
    offset_date = None,
    offset_id = 0,
    offset_peer = InputPeerEmpty(),
    limit = 200,
    hash = 0
))

client.send_message('me', 'Hello, myself!')

for chat in result.chats:
    if target_id == int(chat.id):
        print('found target_id')
        if type(chat) == Chat:
            target_entity = InputPeerChat(chat.id)
        if type(chat) == Channel:
            target_entity = InputPeerChannel(chat.id, chat.access_hash)

for chat in result.chats:
    if type(chat) == Chat:
        chat_groups.append(chat)
    elif type(chat) == Channel:
        channel_groups.append(chat)

print('\nChats')
for chat in chat_groups:
    print(chat)

print("\nChannel")
for channel in channel_groups:
    print(channel)

@client.on(events.NewMessage)
async def handler(event):
    peer_id = event.message.peer_id
    message = event.message.message
    sender = await event.get_sender()

    id: int
    if hasattr(peer_id, 'channel_id'):
        id = peer_id.channel_id

    elif hasattr(peer_id, 'chat_id'):
        id = peer_id.chat_id

    if (id != target_id) & (sender.bot == False):
        print(peer_id, "username", sender.username, message)
        if (type(target_entity) == InputPeerChannel):
            try:
                result = await client(InviteToChannelRequest(
                    channel = target_id,
                    users = [sender.id]
                ))
                # print('Join success to channel', result)
                print('Join success to channel')
            except ChatAdminRequiredError as error:
                print('Add user channel group error', error)
            except UserPrivacyRestrictedError as error:
                print('Add user channel group error', error)
            except PeerFloodError as error:
                print('Add user channel group error', error)
        
        elif (type(target_entity) == InputPeerChat):
            try:
                result = await client(AddChatUserRequest(
                    chat_id = target_id,
                    user_id = sender.id,
                    fwd_limit = 10
                ))
                # print('Join success to chat', result)
                print('Join success to chat')
            except UserAlreadyParticipantError as error:
                print('User are already participated chat group', error)

client.run_until_disconnected()
