import collections
import os
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

options = ChromeOptions()


def chrome_options(chrome_options: ChromeOptions):
    default_preferences = {"download.prompt_for_download": False,
                           "download.default_directory": os.path.expanduser("~/Downloads"),
                           "extensions.ui.developer_mode": False}
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.set_capability('loggingPrefs', {'browser': 'All'})
    chrome_options.add_experimental_option("prefs", default_preferences)
    return chrome_options


def get_page_soup():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options(options))
    url = 'https://joyreactor.cc/post/5276063'
    driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": [
        "http://counter.yadro.ru/hit;JoyReactor?t26.6;r;s1792*1120*30;uhttp%3A//joyreactor.cc/;0.5872430842418059"]})
    driver.execute_cdp_cmd('Network.enable', {})
    driver.get(url)
    rendered_html = driver.page_source
    soup = BeautifulSoup(rendered_html, 'html.parser')
    return soup


def get_messages(soup):
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
        images = post_content.findAll(re.compile(r'(img|iframe|i|source)'))
        for image in images:
            content_data = ''
            if image.name == 'img':
                if image.parent.name != 'video':
                    content_data = image.get('src')
            elif image.name == 'iframe':
                content_data = image.get('src')
            elif image.name == 'i':
                content_data = image.text
            elif image.name == 'source':
                if image.get('type') == 'video/mp4':
                    content_data = image.get('src')
            if len(content_data.strip()) > 0:
                result[link_id].append(content_data)
    return result


def get_m():
    return get_messages(get_page_soup())
