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


url = 'http://joyreactor.cc/tag/coub'
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
    for content in post_content.findAll('div'):
        content_data = ''
        if content.get("class") is not None:
            images = content.findAll(re.compile(r'(a|img|iframe)'))
            attr_type = 'href'
            for image in images:
                if image.name == 'a':
                    attr_type = 'href'
                elif image.name == 'img':
                    attr_type = 'src'
                elif image.name == 'iframe':
                    attr_type = 'src'
                content_data = image.get(attr_type)
        else:
            content_data = content.text
        if len(content_data) > 0:
            result.get(link_id).append(content_data)
print(result)
