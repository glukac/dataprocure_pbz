
from msilib.schema import CompLocator
from db import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY


class Auction(Base):
    __tablename__ = 'auction'
    __table_args__ = {'schema': 'pbz'}

    id = Column(UUID(as_uuid=True), nullable=False)

    pbz_id = Column(Integer, nullable=False)

    client_id = Column(UUID(as_uuid=True), ForeignKey('pbz.client.id'))

    category_id = Column(Integer, nullable=True)

    template = Column(Integer, nullable=True)

    template_name = Column(String, nullable=True)

    is_testing = Column(Boolean, nullable=False)

    is_public = Column(Boolean, nullable=False)

    is_signature_enabled = Column(Boolean, nullable=False)

    type = Column(String, nullable=True)

    type_specification = Column(String, nullable=True)

    languages = Column(ARRAY(String), nullable=True)

    name = Column(JSONB, nullable=True)

    raw_body = Column(JSONB, nullable=False)

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
