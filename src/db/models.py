from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, Numeric, String, BigInteger, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.connections import Base


class User(Base):
    __tablename__ = 'users'

    profile_id = Column(BigInteger, index=True, primary_key=True, unique=True)
    username = Column(String)
    image_url = Column(String, nullable=True, default=None)


class OpenCase(Base):
    __tablename__ = "open_cases"

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    profile_id = Column(BigInteger, index=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    is_active = Column(Boolean, default=False)


class Item(Base):
    __tablename__ = "items"

    profile_id = Column(BigInteger, index=True)
    asset_id = Column(BigInteger, primary_key=True)
    class_id = Column(BigInteger, nullable=True, default=None)
    instance_id = Column(BigInteger, nullable=True, default=None)
    name = Column(String, nullable=True, default=None)
    item_type = Column(String, nullable=True, default=None)
    weapon = Column(String, nullable=True, default=None)
    exterior = Column(String, nullable=True, default=None)
    rarity = Column(String, nullable=True, default=None)
    rarity_color = Column(String, nullable=True, default=None)
    image_url = Column(String, nullable=True, default=None)
    price = Column(Numeric, nullable=True, default=None)
    item_float = Column(Numeric, nullable=True, default=None)
    is_shown = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow())
    open_case_uuid = Column(UUID, ForeignKey(OpenCase.uuid))
    open_case = relationship('OpenCase', viewonly=True, lazy="joined")
