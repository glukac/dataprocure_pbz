import uuid
from datetime import datetime

from db import Base
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

RAW_TYPES = {
    'CATEGORY': 'category',
    'CLIENT': 'client',
    'PARTICIPANT': 'participant',
    'AUCTION': 'auction'
}


class Raw(Base):
    __tablename__ = 'raw'
    __table_args__ = {'schema': 'pbz'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    raw_type = Column(String, nullable=False)

    pbz_id = Column(Integer, nullable=False)

    domain = Column(String, nullable=False)

    body = Column(JSONB, nullable=False)

    created_at = Column(DateTime, nullable=False)

    updated_at = Column(DateTime)

    @classmethod
    def find_one(cls, domain, raw_type, pbz_id, session):
        return session.query(cls).filter_by(
            domain=domain, raw_type=raw_type, pbz_id=pbz_id).order_by(
                Raw.created_at.desc()
        ).first()

    @classmethod
    def find_all_distinct(cls, domain, raw_type, session):
        return session.query(cls).distinct(cls.pbz_id).filter_by(
            domain=domain,
            raw_type=raw_type
        ).order_by(
            cls.pbz_id,
            cls.created_at.desc()
        ).all()

    def __init__(self, raw_type, pbz_id, domain, body) -> None:
        self.raw_type = raw_type
        self.pbz_id = pbz_id
        self.domain = domain
        self.body = body
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        return 'Raw(id={id}, raw_type={raw_type}, domain={domain})'.format(
            id=self.id, raw_type=self.raw_type, domain=self.domain
        )
