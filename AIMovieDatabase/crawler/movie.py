import requests
from bs4 import BeautifulSoup

# 模拟的header
headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/56.0.2924.87 Safari/537.36'}


def crawl_movies():
    origin_url = 'http://maoyan.com'
    movies_info = []
    r = requests.get(origin_url, headers=headers)
    content = r.text
    soup = BeautifulSoup(content, 'lxml')

    # 所有在映电影的url
    movies_url = []
    movie_list = soup.find(class_='movie-list')
    movie_items = movie_list.find_all(class_='movie-item')
    for movie_item in movie_items:
        movies_url.append(movie_item.find('a')['href'])

    url_prefix = 'http://maoyan.com'
    for movie_url in movies_url:
        # 拼接字符串，得到每个电影的url
        r = requests.get(url_prefix + movie_url, headers=headers)
        content = r.text
        soup = BeautifulSoup(content, 'lxml')

        # 中文名
        name = soup.find(class_='name').get_text()
        # 英文名
        en_name = soup.find(class_='ename ellipsis').get_text()
        # 类型
        type = soup.find_all(class_='ellipsis')[1].get_text()
        # 地区时间
        area = soup.find_all(class_='ellipsis')[2].get_text()
        # 上映
        release = soup.find_all(class_='ellipsis')[3].get_text()

        movies_info.append({
            "name": name,
            "en_name": en_name,
            "type": type.split(','),
            "area": area.replace('\n', '').replace(' ', '').split('/')[0],
            "duration": area.replace('\n', '').replace(' ', '').split('/')[1],
            "release": release[:10]
        })
    return movies_info


# print(crawl_movies())
