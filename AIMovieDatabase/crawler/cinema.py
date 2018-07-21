import requests
from bs4 import BeautifulSoup

# 模拟的header
headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/56.0.2924.87 Safari/537.36'}

# 影院的地址，目前为手写，后面可以自动爬取
cinemas_url = ['http://maoyan.com/cinema/9176?poi=5612122']
# 'http://maoyan.com/cinema/62?poi=1078453',
# 'http://maoyan.com/cinema/23763?poi=159444585',
# 'http://maoyan.com/cinema/13398?poi=52210823',
# 'http://maoyan.com/cinema/9500?poi=4132786']

cinemas_info = []


def crawl_cinemas():
    for cinema_url in cinemas_url:
        r = requests.get(cinema_url, headers=headers)
        content = r.text
        soup = BeautifulSoup(content, 'lxml')

        # 影院名字
        cinema_name = soup.find(class_='name text-ellipsis').get_text()
        # 影院地址
        cinema_address = soup.find(class_='address text-ellipsis').get_text()
        # 影院电话
        cinema_phone = soup.find(class_='telphone').get_text()

        # 上映的电影信息
        movies = []
        movies_info = soup.find_all(class_='show-list')
        for movie_info in movies_info:
            # 电影名字，作为电影表的外键
            movie_name = movie_info.find(class_='movie-name').get_text()
            # 电影每天的场次
            screenings = []
            movie_dates_info = movie_info.find_all(class_='plist-container')
            dates = movie_info.find(class_='show-date')
            for (i, movie_date_info) in enumerate(movie_dates_info):  # 一天内的电影的所有场次
                screenings_in_one_day = movie_date_info.find('tbody')
                if screenings_in_one_day:
                    screenings_in_one_day = screenings_in_one_day.find_all('tr')
                    for screening_in_one_day in screenings_in_one_day:
                        # 日期
                        date = dates.find_all('span')[i + 1].get_text()
                        # 开始时间
                        start_time = screening_in_one_day.find(class_='begin-time').get_text()
                        # 结束时间
                        end_time = screening_in_one_day.find(class_='end-time').get_text()
                        # 语言
                        language = screening_in_one_day.find(class_='lang').get_text()
                        # 放映厅
                        hall = screening_in_one_day.find(class_='hall').get_text()
                        # 价格
                        # price = screening_in_one_day.find(class_='price').get_text()

                        # 一场电影
                        screenings.append({
                            "date": date,
                            "start_time": start_time,
                            "end_time": end_time,
                            "language": language,
                            "hall": hall,
                            # "price": price
                        })

            movies.append({
                "movie_name": movie_name,
                "movie_dates_info": screenings
            })

        cinemas_info.append({
            "cinema_name": cinema_name,
            "cinema_address": cinema_address,
            "cinema_phone": cinema_phone,
            "movies": movies
        })
    return cinemas_info
# print(cinemas_info)
