from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship


SERVER = 'DESKTOP-59P7NBL'
DATABASE = 'Pavlo_Python'
DRIVER = 'SQL Server Native Client 11.0'
USERNAME = 'Pavlo'
PASSWORD = '123456'


DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'


engine = create_engine(DATABASE_CONNECTION)

metadata = MetaData(engine)

Base = declarative_base(metadata)


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    password = Column(String(64))
    email = Column(String(64))
    attended_events = relationship("Event", secondary=lambda: user_events_table, back_populates="attendees")
    created_events = relationship("Event", order_by=lambda: Event.id, back_populates="author")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Event(Base):
    __tablename__ = 'Event'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(64))
    date = Column('date', DateTime())
    description = Column(String(512))
    author_id = Column(Integer, ForeignKey('User.id'))
    author = relationship('User', back_populates="created_events")
    attendees = relationship('User', secondary=lambda: user_events_table, back_populates='attended_events')

    def __init__(self, name, date, description, author):
        self.name = name
        self.date = date
        self.description = description
        self.author = author


user_events_table = Table('User_Events', Base.metadata,
                          Column('user_id', Integer, ForeignKey("User.id"),
                                 primary_key=True),
                          Column('event_id', Integer, ForeignKey("Event.id"),
                                 primary_key=True)
                          )

#Base.metadata.create_all(engine)
