from typing import List, Tuple

from telethon.tl.types import Channel, Message
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import db_configuration as db
from sqlalchemy.orm import Session
from classification import *
from logger import Logger


async def read_channel(client: TelegramClient, channel_entity: Channel, msg_num: int,
                       mark_read: bool = False) -> List[Tuple[Message, str]]:
    """Get messages from the channel"""
    msg_list = list()

    async for msg in client.iter_messages(channel_entity, limit=msg_num):
        if msg.message is not None and msg.message != '':
            msg_list.append(msg)
        if mark_read:
            await msg.mark_read()

    classifier = Classifier()

    text_classes = classifier.predict(DataFrame.from_dict({"text": [msg.message for msg in msg_list]}))

    Logger().info(f'Successfully read {len(msg_list)} from {channel_entity.title} channel')

    return list(zip(msg_list, text_classes))


async def add_channel(client: TelegramClient, channel_link: str, msg_num: int = 100):
    """Adds new channel to database and reads latest msg_num messages"""
    session = Session(bind=db.engine)
    try:
        tg_channel = await client.get_entity(channel_link)

        if type(tg_channel) is Channel:

            if session.query(db.Channel).where(db.Channel.tg_link == channel_link).first():
                Logger().warning(f"Channel '{channel_link}' is already saved. New messages won't be loaded")
                return

            new_channel = db.Channel(title=tg_channel.title, tg_link=channel_link)

            session.add(new_channel)
            session.commit()

            msg_list = await read_channel(client, tg_channel, msg_num, mark_read=True)
            # Subscribing channel for future checking
            await client(JoinChannelRequest(tg_channel))
            Logger().info(f"Successfully subscribed channel '{channel_link}'")

            await save_messages(tg_channel.title, msg_list)

        else:
            raise ValueError(f'Entity with link {channel_link} is not a channel')

    except ValueError as e:
        # Channel doesn't exist
        Logger().exception(f"Channel with link {channel_link} doesn't exist")
        pass


async def save_messages(channel_name: str, msg_list: List[Tuple[Message, str]]):
    """Saves messages to database"""
    session = Session(bind=db.engine)
    targ_channel: db.Channel
    targ_channel = session.query(db.Channel).where(db.Channel.title == channel_name).first()

    for msg, text_class in msg_list:
        t_message = db.Message(text=msg.message, text_class=text_class)
        targ_channel.messages.append(t_message)
        # Adding to database
        session.add(t_message)

    session.commit()
    Logger().info(f'{len(msg_list)} new messages from {channel_name} were saved successfully')


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

    Logger().info(f"Found {len(result)} unread channels: {[item[0].title for item in result]}")

    return result
