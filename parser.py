from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from pyvirtualdisplay import Display


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
result = dict()
for post in res_soup:
    link = post.find("a", {"class": 'link'})
    link_id = link.get("href")
    print(link.get("href"))
    result[link_id] = list()
    post_content = post.find("div", {"class": 'post_content'})
    for content in post_content.findAll('div'):
        content_data = ''
        if content.get("class") is not None:
            images = content.findAll("a")
            for image in images:
                content_data = image.get("href")
        else:
            content_data = content.text
        result.get(link_id).append(content_data)
print(result)
