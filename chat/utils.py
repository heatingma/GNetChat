import re
from bs4 import BeautifulSoup
import requests
import favicon
import threading
import time
import func_timeout
from func_timeout import func_set_timeout


def is_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    match = pattern.search(text)
    return match is not None




@func_set_timeout(0.5) # 设置函数最大执行时间
def _download_favicon(url, save_path):
    # if download_url_img(url, save_path) == False:
    try:
        icons = favicon.get(url)
        icon = icons[0]
        response = requests.get(icon.url, stream=True)
        with open(save_path, 'wb') as image:
            for chunk in response.iter_content(1024):
                image.write(chunk)
    except:
        return False
 
 
def download_favicon(url, save_path):
    try:
        if _download_favicon(url, save_path):
            return True
        return False
    except:
        return False


def download_url_img(url:str, save_path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.2; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/30.0.1599.17 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=1)
    except:
        return False
    soup = BeautifulSoup(response.text, "html.parser")
    favicon = soup.find(
        "link", href=True,  rel=lambda x: x and "icon" in x
    )
    if favicon:
        favicon = favicon["href"]
    else:
        return False
    if favicon.startswith("//"):
        favicon = "https:" + favicon
    elif favicon.startswith("/"):
        favicon = url + favicon
    if favicon:
        favicon_resp = requests.get(favicon, headers=headers)
        with open(save_path, "wb") as f:
            f.write(favicon_resp.content)