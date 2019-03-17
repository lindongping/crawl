import requests
from urllib.parse import urlencode

#加载单个Ajax请求
def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    response = requests.get(url)
    return response.json()
#print(get_page('0'))

#解析：提取每条数据的每一张图片的链接
def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                yield {
                    'image' :image.get('url'),
                    'title':title
                }

