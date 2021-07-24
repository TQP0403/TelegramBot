import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
USER_NAME = os.getenv('USER_NAME')

client = TelegramClient(USER_NAME, API_ID, API_HASH)

client.connect()

last_date = None
chunk_size = 200
chats = []
groups = []
participants = []
user_to_remove = []

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
        if chat.megagroup == True:
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

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

print('Fetching Members...')

participants = client.get_participants(target_group, aggressive=True)

for user in participants:
    if not user.is_self:
        print(user)
        user_to_remove.append(client.get_input_entity(user))
        client(EditBannedRequest(target_group_entity, user, ChatBannedRights(
            until_date=None,
            view_messages=True,
        )))



