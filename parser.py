from bs4 import BeautifulSoup
import sys
import re
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from pyvirtualdisplay import Display
import collections


class Client(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


url = 'http://joyreactor.cc/'
with Display(visible=0, size=(800, 600)):
    rendered_html = Client(url).html
soup = BeautifulSoup(rendered_html, 'html.parser')
res_soup = soup.findAll("div", {"class": 'postContainer'})
result = collections.OrderedDict()
for post in res_soup:
    link = post.find("a", {"class": 'link'})
    link_id = link.get("href")
    result[link_id] = list()
    post_content = post.find("div", {"class": 'post_content'})
    for i in post_content.findAll(text=True):
        if i == "FixGifVideo()" or i == "ссылка на гифку":
            i.replace_with("")
        else:
            i.wrap(soup.new_tag('i'))
    images = post_content.findAll(re.compile(r'(a|img|iframe|i)'))
    for image in images:
        content_data = ''
        if image.name == 'a':
            if image.get("class") is not None:
                if 'prettyPhotoLink' not in image.get('class'):
                    content_data = image.get('href')
            else:
                href = image.get('href')
                if "diyGif" not in href:
                    content_data = href
        elif image.name == 'img':
            if image.parent.name != 'video':
                content_data = image.get('src')
        elif image.name == 'iframe':
            content_data = image.get('src')
        elif image.name == 'i':
            content_data = image.text
        if len(content_data) > 0:
            result[link_id].append(content_data)

print(result)
