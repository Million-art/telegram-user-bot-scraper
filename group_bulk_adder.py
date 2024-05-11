from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

# Replace with your own API credentials
api_id = 'your api id'
api_hash = 'your api hash'

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Replace with the username of the source channel
source_channel_username = '@your surce channel username'

# Replace with the username of the destination channel
destination_channel_username = '@your destination channel username'

# Function to fetch members from the source channel and add them to the destination channel
async def add_members_to_destination_channel():
    try:
        # Connect to Telegram
        await client.start()

        # Resolve the source channel username to its ID
        source_entity = await client.get_entity(source_channel_username)
        source_channel_id = source_entity.id

        # Resolve the destination channel username to its ID
        destination_entity = await client.get_entity(destination_channel_username)
        destination_channel_id = destination_entity.id

        # Fetch members from the source channel
        members = await client.get_participants(source_channel_id, limit=1000)

        # Filter out bots from the list of members
        members = [member for member in members if not member.bot]

        # Invite each non-bot member to the destination channel
        for member in members:
            try:
                await client(InviteToChannelRequest(
                    channel=destination_channel_id,
                    users=[member]
                ))
                print(f"Added Member: {member.first_name} {member.last_name}")
            except Exception as e:
                print(f"Error adding member {member.first_name} {member.last_name}: {e}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Disconnect from Telegram
        await client.disconnect()

# Call the function to add members from the source channel to the destination channel
client.loop.run_until_complete(add_members_to_destination_channel())
