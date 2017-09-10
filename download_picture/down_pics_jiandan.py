import urllib.request
import os

"""
到煎蛋网爬取图片数据
"""


def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User_Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) '
                   'Chrome/59.0.3071.115 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()

    return html


def get_page(url):
    html = url_open(url).decode('utf-8')

    a = html.find('current-comment-page') + 23
    b = html.find(']', a)

    return html[a:b]


def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []

    a = html.find('src=')

    while a != -1:
        b = html.find('.jpg', a, a + 255)
        if b != -1:
            img_addrs.append('http:' + html[a + 5:b + 4])
        else:
            b = a + 5

        a = html.find('src=', b)
    for each in img_addrs:
        print(each)
    return img_addrs


def save_imgs(folder, img_addrs):
    for each in img_addrs:
        file_name = each.split('/')[-1]
        with open(file_name, 'wb') as f:
            img = url_open(each)
            f.write(img)


def down_mm(folder='OOXX', pages=10):
    os.mkdir(folder)
    os.chdir(folder)

    url = "http://jandan.net/ooxx/"
    page_num = int(get_page(url))

    for i in range(pages):
        page_num -= i
        page_url = url + 'page-' + str(page_num) + '#comments'
        img_addrs = find_imgs(page_url)
        save_imgs(folder, img_addrs)


if __name__ == '__main__':
    down_mm()
