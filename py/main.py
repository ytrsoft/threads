from sqlite import get_db, Post
from sqlalchemy import func

if __name__ == '__main__':
  db = next(get_db())
  posts = db.query(Post).order_by(func.random()).limit(10).all()
  print(len(posts))
  for post in posts:
    print(post.id, post.title)

