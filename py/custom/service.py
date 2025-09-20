from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlite import Post, Category, Image, get_db, init_db

init_db()

def get_categories():
  db: Session = next(get_db())
  return db.query(
    Category.id,
    Category.title,
    func.count(Post.id).label('value')
  ).join(
    Post, Category.id == Post.mid
  ).group_by(
    Category.id, Category.title
  ).having(
    func.count(Post.id) > 0
  ).order_by(
    func.count(Post.id).desc()
  ).all()

def get_posts(page, size, cid=None, keyword=None):
  db: Session = next(get_db())
  query = db.query(Post)
  if cid:
    query = query.filter(Post.mid == cid)
  if keyword:
    search = f"%{keyword}%"
    query = query.filter(
      Post.title.like(search) |
      Post.desc.like(search) |
      Post.region.like(search) |
      Post.age.like(search) |
      Post.score.like(search) |
      Post.price.like(search) |
      Post.service.like(search)
    )

  total_count = query.count()
  offset = (page - 1) * size
  posts = query.offset(offset).limit(size).all()
  has_more = offset + len(posts) < total_count
  return posts, has_more
