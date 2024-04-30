import logging
import traceback
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from telethon.errors import FloodWaitError
import asyncio
import json

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='w')
logger = logging.getLogger()


# Telegram API credentials
telegram_api_id = 22164421
telegram_api_hash = 'e911332999d3e9d1fc308b0dff7797bc'

# Initialize Telegram client
telegram_client = TelegramClient('session_name', telegram_api_id, telegram_api_hash)


# Function to read last post IDs from file
def read_last_post_ids():
    try:
        with open('last_post_ids.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Function to save last post IDs to file
def save_last_post_ids(last_post_ids):
    with open('last_post_ids.json', 'w') as file:
        json.dump(last_post_ids, file)


# Function to check for new messages and repost them
async def check_and_repost_messages():
    try:
        await telegram_client.start()

        source_channel_usernames = ['@LinosBonda07', '@promomoye', '@nejashionlinemarketing', '@Adeybonda', '@merkato101', '@qnashcom', '@shopingett', '@shegershoes123', '@geezshoes','@hamdbrand','@Hilumart6','@technologycfy']
        destination_channel_username = 'https://t.me/inbivili'
        last_post_ids = read_last_post_ids()
        while True:
            for source_channel_username in source_channel_usernames:
                try:
                    source_entity = await telegram_client.get_entity(source_channel_username)
                    source_channel_id = source_entity.id
                    messages = await telegram_client.get_messages(source_channel_id, limit=1)
                    if messages:
                        last_message = messages[0]
                        last_message_id = last_message.id
                        if source_channel_username not in last_post_ids or last_post_ids[source_channel_username] != last_message_id:
                            repost_message = f"From: {source_channel_username}\n"

                            if last_message.text:
                                repost_message += f"\n{last_message.text}"

                            if isinstance(last_message.media, MessageMediaPhoto):
                                photo = last_message.media.photo
                                await telegram_client.send_file(destination_channel_username, photo, caption=repost_message)
                                logger.debug(f"Last message with photo from {source_channel_username} reposted successfully.")

                            else:
                                repost_message += f"\n\nSource Channel: {source_channel_username}"
                                await telegram_client.send_message(destination_channel_username, repost_message)
                                logger.debug(f"Last message without photo from {source_channel_username} reposted successfully.")
                            last_post_ids[source_channel_username] = last_message_id
                            save_last_post_ids(last_post_ids)
                except FloodWaitError as e:
                    logger.error(f"Error: Flood wait. Waiting for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)
                    continue
                except Exception as e:
                    logger.error(f"Error reposting last message from {source_channel_username}: {e}")
                    traceback.print_exc()

            # Sleep for 5 seconds before checking again
            await asyncio.sleep(5)
    except Exception as e:
        logger.error(f"Error reposting last message: {e}")
        traceback.print_exc()
    finally:
        await telegram_client.disconnect()


# Run the function only if this is the main module being executed
if __name__ == "__main__":
    asyncio.run(check_and_repost_messages())