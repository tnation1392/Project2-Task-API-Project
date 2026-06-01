from sqlalchemy import Column, String
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    api_key = Column(String, nullable=False, unique=True, index=True)