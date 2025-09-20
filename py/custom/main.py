import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget
from decorator import QtWindow
from widgets import CategoryMenu, PostList, SearchWidget
from service import get_categories, get_posts

class MainWindow(QtWindow):
  def __init__(self):
    super().__init__()
    self.cid = None
    self.keyword = None
    self.new_window = None
    self.set_title('主窗体')

    categories = get_categories()
    lefy_menu = CategoryMenu(categories)
    lefy_menu.category_selected.connect(self.on_selected)

    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(16)

    search = SearchWidget()
    search.search_triggered.connect(self.on_search)
    content_layout.addWidget(search)

    self.post_list = PostList()
    self.post_list.page_change.connect(self.load_page)
    content_layout.addWidget(self.post_list, 1)

    list_widget = QListWidget()
    content_layout.addWidget(list_widget, 8)

    self.main_layout.addWidget(lefy_menu, 2)
    self.main_layout.addWidget(content, 8)

  def on_selected(self, e):
    self.cid = e
    self.post_list.refresh()

  def on_search(self, e):
    self.keyword = e
    self.post_list.refresh()

  def load_page(self, page):
    posts, has_more = get_posts(page, 10, self.cid, self.keyword)
    self.post_list.set_posts(posts, has_more)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
