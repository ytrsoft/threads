from sqlite import get_db, Post

if __name__ == '__main__':
    db = next(get_db())
    posts = db.query(Post).all()
    print(len(posts))
