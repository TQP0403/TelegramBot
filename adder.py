import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE1')

client = TelegramClient(PHONE, API_ID, API_HASH)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(PHONE)
    client.sign_in(PHONE, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 200
groups = []
participants = []
user_to_add = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except:
        continue

# print('Choose a group to scrape members from:')
i = 0
for g in groups:
    print(str(i) + '/ ' + g.title)
    print(g)
    i += 1

# g_index = input("Enter a Number: ")
# target_group = groups[int(g_index)]
target_group = groups[0]
main_group = groups[1]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

print('Fetching Members...')

participants = client.get_participants(main_group, aggressive=True)

for user in participants:
    print(user)
    user_entity = client.get_input_entity(user)
    user_to_add.append(client.get_input_entity(user))

client(InviteToChannelRequest(target_group_entity, user_to_add))
