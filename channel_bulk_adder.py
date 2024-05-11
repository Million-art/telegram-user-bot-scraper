import csv
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

# Replace with your own API credentials
api_id = 22164421
api_hash = 'e911332999d3e9d1fc308b0dff7797bc'

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Replace with the username or ID of the channel
channel_username = '@asffeee'

# Function to invite members to the channel using phone numbers from a CSV file
async def invite_members_from_csv():
    try:
        # Connect to Telegram
        await client.start()

        # Read phone numbers from CSV file
        with open('phone_numbers.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                phone_number = row[0].strip()  # Get the phone number and remove any whitespace
                if phone_number.startswith('+'):  # Ensure the phone number is in international format
                    await client(InviteToChannelRequest(
                        channel=channel_username,
                        users=[phone_number]
                    ))
                    print(f"Invited user with phone number: {phone_number}")
                else:
                    print(f"Invalid phone number format: {phone_number}")

    except Exception as e:
        print(f"Error inviting members: {e}")

    finally:
        # Disconnect from Telegram
        await client.disconnect()

# Call the function to invite members from the CSV file to the channel
client.loop.run_until_complete(invite_members_from_csv())
