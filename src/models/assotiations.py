from db import Base
from sqlalchemy import Column, ForeignKey, Table

client_participant = Table('client_participant',
    Base.metadata,
    Column('client_id', ForeignKey('pbz.client.id')),
    Column('participant_id', ForeignKey('pbz.participant.id')),
    schema='pbz'
)

auction_participant = Table('auction_participant',
    Base.metadata,
    Column('auction_id', ForeignKey('pbz.auction.id')),
    Column('participant_id', ForeignKey('pbz.participant.id')),
    schema='pbz'
)