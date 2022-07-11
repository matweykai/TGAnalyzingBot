from typing import List, Tuple

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import Channel, Message
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import db_configuration as db
from sqlalchemy.orm import Session


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


async def add_channel(client: TelegramClient, channel_link: str, msg_num: int = 100):
    """Adds new channel to database and reads latest msg_num messages"""
    session = Session(bind=db.engine)
    try:
        tg_channel = await client.get_entity(channel_link)

        if type(tg_channel) is Channel:

            if session.query(db.Channel).where(db.Channel.tg_link == channel_link).first():
                # TODO: add logging or raising exception
                return

            new_channel = db.Channel(title=tg_channel.title, tg_link=channel_link)

            session.add(new_channel)
            session.commit()

            msg_list = await read_channel(client, tg_channel, msg_num)
            # Subscribing channel for future checking
            await client(JoinChannelRequest(tg_channel))
            # TODO: add logging bot subscription

            await save_messages(tg_channel.title, msg_list)

        else:
            raise ValueError(f'Entity with link {channel_link} is not a channel')

    except ValueError:
        # Channel doesn't exist
        # TODO: add logging or exception raising
        pass


async def save_messages(channel_name: str, msg_list: List[Message]):
    """Saves messages to database"""
    session = Session(bind=db.engine)
    targ_channel: db.Channel
    targ_channel = session.query(db.Channel).where(db.Channel.title == channel_name).first()

    for msg in msg_list:
        t_message = db.Message(text=msg.message)
        targ_channel.messages.append(t_message)
        # Adding to database
        session.add(t_message)
        # TODO: add logging for the new messages

    session.commit()
    # TODO: add logging on successfull saving


async def get_unread_channels(client: TelegramClient) -> List[Tuple[Channel, int]]:
    """Returns channels that have unread messages"""
    result = list()

    session = Session(bind=db.engine)
    # Collecting target channels titles
    targ_channels_titles = [item.title for item in session.query(db.Channel).all()]

    async for dialog in client.iter_dialogs():
        if not dialog.is_group and dialog.is_channel:
            unread_count = dialog.unread_count
            temp_channel = await client.get_entity(dialog.entity)
            # Adding target channels with unread messages to the result
            if unread_count != 0 and temp_channel.title in targ_channels_titles:
                result.append((temp_channel, unread_count))

    # TODO: add logging on successfull getting unread channels

    return result
