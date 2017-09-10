import requests
import bs4
from bs4 import BeautifulSoup


def get_page(page_num):
    page_urls = []
    url = 'http://college.gaokao.com/schlist/p'
    for i in range(1, page_num + 1):
        u = url + str(i) + '/'
        page_urls.append(u)
    return page_urls


def get_html(url):
    try:
        header = {'User_Agent':
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36'}
        page = requests.get(url, headers=header, timeout=60)
        page.raise_for_status()
        page.encoding = page.apparent_encoding
        return page.text
    except:
        return 'error'


def get_each_info(html):
    # info_each_page = []
    # end = 0
    # for i in range(25):
    #     info = []
    #     start_part = 'target="_blank"><img src="'
    #     start = html.find(start_part, end) + len(start_part)
    #     end = html.find('"', start)
    #     url = html[start:end]
    #     start_part2 = 'strong title="'
    #     start = html.find(start_part2, end) + len(start_part2)
    #     end = html.find('"', start)
    #     name = html[start:end]
    #     start_part3 = '学校网址：'
    #     start = html.find(start_part3, end) + len(start_part3)
    #     end = html.find('<', start)
    #     uni_url = html[start: end]
    #     info.append(url)
    #     info.append(name)
    #     info.append(uni_url)
    #     info_each_page.append(info)
    # return info_each_page
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find_all(id='wrapper')
    uni_list = []
    global dls
    for each in info:
        if isinstance(each, bs4.element.Tag):
            dls = each('dl')
    for each in dls:
        uni = []
        item = each('dt')[0]('a')[0]('img')[0]
        img_url = item.attrs['src']
        name = item.attrs['alt']
        # dls[0]('li')[-1].string[5:]
        uni_url = each('li')[-1].string[5:]
        uni.append(name)
        uni.append(uni_url)
        uni.append(img_url)
        uni_list.append(uni)
    return uni_list


def get_all_info(page_num):
    all_info = []
    page_urls = get_page(page_num)
    for each in page_urls:
        html = get_html(each)
        all_info.extend(get_each_info(html))
    return all_info


#
# def get_img_urls(all_info, page_num):
#     img_urls = []
#     for i in range(25 * page_num):
#         img_urls.append(all_info[i][0])
#     return img_urls


def url_format(all_info):
    for i in range(len(all_info)):
        if all_info[i][1][0] != 'h':
            all_info[i][1] = 'http://' + all_info[i][1]
        if all_info[i][1][-1] != '/':
            all_info[i][1] += '/'
    return all_info


# def save_imgs(all_info):
#     img_urls = get_img_urls(all_info)
#     for i in range(500):
#         path = 'logo/' + all_info[i][1] + '.png'
#         r = requests.get(img_urls[i])
#         with open(path, 'wb') as f:
#             f.write(r.content)
# def save_info(all_info):
#     url_format(all_info)
#     file_name = 'info.txt'
#     for i in range(500):
#         with codecs.open(file_name, 'a', 'utf-8') as f:
#             f.write(all_info[i][1] + '        主页:' + all_info[i][2] + '\r\n')


def main():
    page_num = 50
    all_info = get_all_info(page_num)
    #database = url_format(all_info)
    # data=[]
    # for item in database:
    #     if item not in data:
    #         data.append(item)
    # print(data)
    # print(len(data))
    # print(len(database))


if __name__ == "__main__":
    main()
