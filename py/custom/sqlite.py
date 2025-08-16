from sqlalchemy import create_engine, Column, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(String, primary_key=True)
    title = Column(String(255))
    posts = relationship('Post', back_populates='category')

class Post(Base):
    __tablename__ = 'post'
    id = Column(String, primary_key=True)
    title = Column(String(255))
    desc = Column(Text)
    region = Column(String(255))
    age = Column(String(50))
    score = Column(String(50))
    price = Column(String(50))
    service = Column(String(255))
    wechat = Column(String(100))
    qq = Column(String(100))
    phone = Column(String(20))
    mid = Column(String, ForeignKey('category.id'))
    category = relationship('Category', back_populates='posts')
    images = relationship('Image', back_populates='post')

class Image(Base):
    __tablename__ = 'image'
    id = Column(String, primary_key=True)
    src = Column(String(255))
    pid = Column(String, ForeignKey('post.id'))
    post = relationship('Post', back_populates='images')

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
