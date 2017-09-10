import requests
import urllib.parse
import threading

# 设置线程锁
thread_lock = threading.BoundedSemaphore(value=10)


# 获取网站页面
def get_page(url):
    page = requests.get(url)
    page = page.content
    page = page.decode('utf-8')
    return page


# 找到每一页中的图片链接
def find_urls_in_page(page, start_part, end_part):
    all_strings = []
    end = 0
    while page.find(start_part, end) != -1:
        start = page.find(start_part, end) + len(start_part)
        end = page.find(end_part, start)
        string = page[start:end]
        all_strings.append(string)
    return all_strings


def pages_from_duitang(label):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=1000'
    label = urllib.parse.quote(label)
    for index in range(0, 3600, 100):
        u = url.format(label, index)
        page = get_page(u)
        pages.append(page)
    return pages


# 字符串的切片
def pic_urls_from_pages(pages):
    pic_urls = []
    for page in pages:
        urls = find_urls_in_page(page, 'path":"', '"')
        pic_urls.extend(urls)
    return pic_urls


def download_pics(url, n):
    r = requests.get(url)
    file_name = url.split('/')[-1]
    path = 'pics/' + file_name
    with open(path, 'wb') as f:
        f.write(r.content)
    # 解锁
    thread_lock.release()


def main(label):
    pages = pages_from_duitang(label)
    pic_urls = pic_urls_from_pages(pages)
    # num=len(pic_urls)
    # print(num)
    n = 0
    for url in pic_urls:
        n += 1
        print('正在下载第{}张图片'.format(n))
        thread_lock.acquire()
        t = threading.Thread(target=download_pics, args=(url, n))
        t.start()


if __name__ == '__main__':
    main('校花')
