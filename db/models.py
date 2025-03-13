from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    name = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
