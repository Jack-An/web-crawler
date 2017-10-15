"""
获得所有Tag的网页
最多获取50页的信息
先不比考虑异常处理
将可能不存在页面放在解析HTML方法中进行异常处理
@get_urls(tag)
@get_all_url()
"""
import requests
import urllib.parse
from bs4 import BeautifulSoup
import time
import re
from get_tag import get_html_text, get_all_tag


#  @all_tag_url(tags)
#  args:标签的列表
#  得到所有传入标签列表的可能存在的url
#  返回传入的tags的url列表
def all_tag_url(tags):
    page_url = []
    for tag in tags:
        page_url.extend(tag_url(tag))
    return page_url


def tag_url(tag):
    url = 'https://book.douban.com/tag/{}?start={}&type=T'
    item = []
    count = 0
    for i in range(50):
        start = url.format(urllib.parse.quote(tag), count)
        count += 20
        item.append(start)
    return item


def get_html(url):
    try:
        header = {'User_Agent':
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36'}
        page = requests.get(url, headers=header, timeout=60)
        page.raise_for_status()
        page.encoding = page.apparent_encoding
        if page.text.find('没有找到符合条件的图书') == -1:
            return page.text
        else:
            return None
    except:
        return None


def parse_html_text(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        information = []
        regex = re.compile(r'豆瓣图书标签:.*?<')
        label = regex.findall(html)[0].split(':')[1][:-1]
        subjects = soup.find_all('li', {'class': 'subject-item'})
        for each in subjects:
            # 里面有好多莫名其妙的错误，所以干脆用try...except
            # 有错误就跳过去
            try:
                full_info_page = each('a')[0].attrs['href']
                title = each('a')[1].attrs['title']
                pub = each.find_all('div', {'class': 'pub'})[0].string.split('\n')[-3]
                if each.find_all('span', {'class': 'rating_nums'}):
                    num_rate = float(each.find_all('span', {'class': 'rating_nums'})[0].string)
                else:
                    num_rate = 0
                if each.find_all('p'):
                    summary = each.find_all('p')[0].string
                else:
                    summary = ''
                comment_num = int(each.find_all('span', {'class': 'pl'})[0].string.split('\n')[-2].split('(')[-1][:-4])
                information.append([title, label, full_info_page, pub, num_rate, summary, comment_num])
            except:
                continue
        return information


# @get_all_url()
# 获取所有的url
def get_all_url():
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    tags = get_all_tag(get_html_text(url))
    print(tags)
    all_url = all_tag_url(tags)
    return all_url




# 异常处理交给HTML页面获取方法
def main():
    database = []
    all_url = get_all_url()
    count = 0
    for url in all_url:
        try:
            each_info = parse_html_text(get_html(url))
            database.extend(each_info)
            count += 1
            if count % 10 == 0:
                time.sleep(30)
            if count % 50 == 0:
                print('已经抓取到{}页面的数据'.format(count))
        except:
            continue
    return database


if __name__ == '__main__':
    pass
   
