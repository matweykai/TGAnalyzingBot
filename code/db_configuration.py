from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from bot_configuration import bot_config


Base = declarative_base()


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    tg_link = Column(String)
    messages = relationship("Message", back_populates="channel")

    def __repr__(self):
        return f"Channel(id={self.id}, title='{self.title}', tg_link='{self.tg_link}')"


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    channel_id = Column(Integer, ForeignKey("channel.id"))
    channel = relationship("Channel", back_populates="messages")

    def __repr__(self):
        return f"Message(id={self.id}, text_len={len(self.text) if self.text is not None else 0}, " \
               f"channel_id={self.channel_id})"


# Using database connection string from .env file
engine = create_engine(bot_config.db_str)
Base.metadata.create_all(engine)
