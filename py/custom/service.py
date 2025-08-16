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
