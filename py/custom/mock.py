from sqlalchemy import create_engine, Column, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
from faker import Faker
import uuid
import random

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

fake = Faker('zh_CN')

def generate_fake_data():
    db = next(get_db())
    categories = []
    category_titles = [
        '美食推荐', '旅游景点', '本地服务', '二手交易', '房屋租赁', '招聘信息', '教育培训',
        '宠物之家', '汽车买卖', '数码产品', '时尚穿搭', '家居装饰', '运动健身', '健康养生',
        '艺术文化', '亲子活动', '婚庆服务', '摄影摄像', '娱乐活动', '公益活动',
        '美食外卖', '夜市小吃', '咖啡茶饮', '甜品蛋糕', '特色餐厅', '民宿体验',
        '户外探险', '城市漫步', '周边游玩', '国际旅行', '家政服务', '维修安装',
        '快递物流', '二手书籍', '电子产品', '服装鞋帽', '珠宝饰品', '健身房推荐',
        '瑜伽课程', '舞蹈培训', '音乐学习', '美术课程', '语言培训', '职业技能',
        '宠物寄养', '宠物用品', '汽车租赁', '二手车交易', '数码配件', '家居用品'
    ]
    for title in category_titles:
        category = Category(
            id=str(uuid.uuid4()),
            title=title
        )
        categories.append(category)
        db.add(category)
    db.commit()
    for category in categories:
        for _ in range(100):
            post = Post(
                id=str(uuid.uuid4()),
                title=fake.sentence(nb_words=6)[:-1],
                desc=fake.paragraph(nb_sentences=5),
                region=fake.city(),
                age=str(random.randint(18, 60)),
                score=str(random.randint(1, 5)),
                price=str(random.randint(50, 5000)),
                service=random.choice(['上门服务', '到店服务', '在线服务', '其他']),
                wechat=fake.user_name(),
                qq=str(random.randint(100000000, 999999999)),
                phone=fake.phone_number(),
                mid=category.id
            )
            db.add(post)
            for _ in range(20):
                image = Image(
                    id=str(uuid.uuid4()),
                    src=f'https://picsum.photos/750/450',
                    pid=post.id
                )
                db.add(image)
    db.commit()
    print('假数据生成完成！')

if __name__ == '__main__':
    init_db()
    generate_fake_data()
