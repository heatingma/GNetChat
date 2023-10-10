import re

def is_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    match = pattern.search(text)
    return match is not None