from typing import List

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import Channel, Message
from telethon import TelegramClient


async def read_channel(client: TelegramClient, channel_entity: Channel, msg_num: int) -> List[Message]:
    """Get messages from the channel"""
    return (await client(GetHistoryRequest(peer=channel_entity,
                                    limit=msg_num,
                                    offset_date=None,
                                    offset_id=0,
                                    max_id=0,
                                    min_id=0,
                                    add_offset=0,
                                    hash=0))).messages
