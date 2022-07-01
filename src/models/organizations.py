import uuid

from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class Client(Base):
    __tablename__ = 'client'
    __table_args__ = {'schema': 'pbz'}

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)

    pbz_id = Column(Integer, nullable=False)

    name = Column(String, nullable=False)

    street = Column(String, nullable=True)

    city = Column(String, nullable=True)

    postal_code = Column(String, nullable=True)

    phone = Column(String, nullable=True)

    fax = Column(String, nullable=True)

    email = Column(String, nullable=True)

    web = Column(String, nullable=True)

    person = Column(String, nullable=True)

    timezone = Column(String, nullable=True)

    country_code = Column(String, nullable=True)

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        
    def __repr__(self) -> str:
        return 'Client(id={id}, name={name})'.format(
            id=self.id, name=self.name
        )

class Participant(Base):
    __tablename__ = 'participant'
    __table_args__ = {'schema': 'pbz'}

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)

    pbz_id = Column(Integer, nullable=False)

    language = Column(String, nullable=False)

    name = Column(String, nullable=False)

    street = Column(String, nullable=True)

    city = Column(String, nullable=True)

    postal_code = Column(String, nullable=True)

    phone = Column(String, nullable=True)

    fax = Column(String, nullable=True)

    email = Column(String, nullable=True)

    web = Column(String, nullable=True)

    person = Column(String, nullable=True)

    timezone = Column(String, nullable=True)

    country_code = Column(String, nullable=True)

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        
    def __repr__(self) -> str:
        return 'Client(id={id}, name={name})'.format(
            id=self.id, name=self.name
        )

    

