import random
import string
import uuid
import base64


def generate_short_uuid():
    # Generate a UUID and remove the hyphens
    uuid_str = uuid.uuid4()

    # Convert UUID to bytes and then encode in Base64
    base64_uuid = base64.urlsafe_b64encode(uuid_str.bytes).decode("utf-8")

    # Truncate the string to 15 characters
    short_uuid = base64_uuid[:15]

    return short_uuid


def generate_custom_id(length=15):
    # Define the characters for the custom ID
    characters = string.ascii_letters + string.digits

    # Randomly select `length` characters from the character set
    custom_id = ''.join(random.choices(characters, k=length))

    return custom_id