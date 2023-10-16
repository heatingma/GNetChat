from bs4 import BeautifulSoup
import requests
import favicon
from argparse import ArgumentParser


###################################################
#                download_favicon                 #
###################################################

def download_favicon(url, save_path):
    try:
        _download_favicon(url, save_path)
    except:
        _download_favicon2(url, save_path)
    

def _download_favicon(url, save_path):
    try:
        icons = favicon.get(url)
        icon = icons[0]
        response = requests.get(icon.url, stream=True)
        with open(save_path, 'wb') as image:
            for chunk in response.iter_content(1024):
                image.write(chunk)
    except:
        return False
 

def _download_favicon2(url:str, save_path):
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
            

def download_arg_parser():
    """
        Arguments for download favicon
    """
    parser = ArgumentParser(description='Arguments for download favicon.')
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--save_path', type=str, required=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = download_arg_parser()
    download_favicon(args.url, args.save_path)

