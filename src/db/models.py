from sqlalchemy import Column, Integer, Boolean, DateTime, Numeric, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from db.connections import Base


class ObservedProfile(Base):
    __tablename__ = "observed_profiles"

    profile_id = Column(BigInteger, unique=True, index=True, primary_key=True)
    last_asset_id = Column(BigInteger, default=0)
    is_observed = Column(Boolean, default=False)
    last_modified_date = Column(DateTime)
    total_amount = Column(Numeric, default=0)
    total_count = Column(Integer, default=0)


class OpenCase(Base):
    __tablename__ = "opencases"
    uuid = Column(UUID, primary_key=True, unique=True)


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



