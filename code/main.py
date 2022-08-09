from telethon import TelegramClient
from bot_functions import read_channel, add_channel, db, get_unread_channels, save_messages
from sqlalchemy.orm import Session
import click as cli
from classification import *
from logger import Logger
import os

# Global client object
client = TelegramClient('anon', bot_config.api_id, bot_config.api_hash)


async def update_handler():
    """Gets messages from unread channels"""
    unread_channels = await get_unread_channels(client)

    for chan_entity, msg_num in unread_channels:
        # Getting pairs of messages and text_classes
        new_msgs = await read_channel(client, chan_entity, msg_num, mark_read=True)
        # Saving pairs to database
        await save_messages(chan_entity.title, new_msgs)


@cli.command()
@cli.option('--add-channel', '-a', 'new_channel', default=None)
@cli.option('--update', '-u', default=None, is_flag=True)
def main(new_channel, update):
    Logger().info(f"Start program from {os.curdir}")

    with client:
        if new_channel is not None:
            # Adding new channel and read 300 latest news from it
            client.loop.run_until_complete(add_channel(client, new_channel, msg_num=300))
        elif update is not None:
            # Updating information in database with unread news
            client.loop.run_until_complete(update_handler())
        else:
            # Show all information from database
            session = Session(bind=db.engine)

            print(session.query(db.Channel).all())
            print(session.query(db.Message).all())

            print(len(session.query(db.Message).where(db.Message.channel_id == 1).all()))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        Logger().critical(e)

    Logger().info('Program finished work')