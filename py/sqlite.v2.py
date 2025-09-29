from sqlalchemy import create_engine, Column, String, Text, Boolean, DateTime, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from datetime import datetime
import uuid

Base = declarative_base()

class BaseEntity(Base):
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    visited = Column(Boolean, default=False)

class Category(BaseEntity):
    __tablename__ = 'category'
    
    title = Column(String(36), nullable=True)

class Image(BaseEntity):
    __tablename__ = 'image'
    
    src = Column(String(255), nullable=True)
    pid = Column(String(36), nullable=True)

class Marker(BaseEntity):
    __tablename__ = 'marker'
    
    cid = Column(String(36), nullable=True)
    pid = Column(String(36), nullable=True)

class Pager(BaseEntity):
    __tablename__ = 'pager'
    
    cid = Column(String(36), nullable=True)
    page = Column(Integer, nullable=True)
    pages = Column(Integer, nullable=True)

class Post(BaseEntity):
    __tablename__ = 'post'
    
    title = Column(String(255), nullable=True)
    desc = Column(Text, nullable=True)
    region = Column(String(36), nullable=True)
    age = Column(String(36), nullable=True)
    score = Column(String(36), nullable=True)
    price = Column(String(36), nullable=True)
    service = Column(String(72), nullable=True)
    wechat = Column(String(36), nullable=True)
    qq = Column(String(36), nullable=True)
    phone = Column(String(36), nullable=True)
    cid = Column(String(36), nullable=True)

DATABASE_URL = 'sqlite:///dataset.sqlite'
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = scoped_session(sessionmaker(bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    