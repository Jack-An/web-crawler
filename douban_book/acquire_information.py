import requests
from bs4 import BeautifulSoup
import bs4


def get_url():
    # https: // book.douban.com / top250?start = 0
    # https: // book.douban.com / top250?start = 0
    start = 0
    urls = []
    for i in range(10):
        url = 'https://book.douban.com/top250?start =' + str(start) + '/'
        urls.append(url)
        start += 25
    return urls


# 利用requests库获取页面
def get_html(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
        page.encoding = page.apparent_encoding
        return page.text
    except:
        return "error"


# 分析HTML页面，利用BeautifulSoup进行数据的抓取
def analyze_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find_all(id='content')
    global tr_tags
    for each in info:
        if isinstance(each, bs4.element.Tag):
            tr_tags = each('tr')
    elements = []
    for each in tr_tags:
        tag = each('td')
        elements.append(tag)
    book_database = []
    for item in elements:
        each_info = []
        full_info_url = item[0]('a')[0].attrs['href']
        book_img = item[0]('img')[0].attrs['src']
        book_name = item[1]('a')[0].attrs['title']
        # 由于豆瓣网评分分布在两个不同的Tag中，所以进行判断
        if item[1]('span')[1].string is None:
            rating_nums = item[1]('span')[2].string
        else:
            rating_nums = float(item[1]('span')[1].string)
        sentence = item[1]('span')[-1].string
        each_info.append(book_name)
        each_info.append(rating_nums)
        each_info.append(book_img)
        each_info.append(full_info_url)
        each_info.append(sentence)
        book_database.append(each_info)

    return book_database


def acquire_info():
    all_info = []
    page_urls = get_url()
    for each in page_urls:
        html = get_html(each)
        #异常处理
        if get_html(each) not is "error"  
            all_info.extend(analyze_html(html))
    return all_info


if __name__ == '__main__':
    data = acquire_info()
    for each in data:
        print(each)
    print(len(data))
