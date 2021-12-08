import requests
from bs4 import BeautifulSoup


# 検索結果から実際のページを取得し，ページ内のダウンロードリンクを表示する
def get_download_urls(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')

    a_tags = soup.select('a[class=autohyperlink]')
    for a in a_tags:
        url = a['href']
        if 'mexa.sh' in url or 'mx-sh.net' in url:
            print(url)


# 検索結果ページから次の検索結果ページを取得する
def get_next_page(soup):
    a_tags = soup.select('a[rel=next]')

    if len(a_tags) > 0:
        a = a_tags[0]
        url = a['href']
        # print(url)
        return url
    else:
        return None


# 検索結果ページを取得する
def get_search_result_urls(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')

    a_tags = soup.select('h2 a')
    for a in a_tags:
        url = a['href']
        # print(url)
        get_download_urls(url)
    next_url = get_next_page(soup)

    # 次のページが存在するなら，再帰的に実行
    if next_url is not None:
        get_search_result_urls(next_url)


if __name__ == '__main__':
    file_name = './input_url_list.txt'
    with open(file_name, 'r', errors='replace', encoding="utf_8") as file:
        line_list = file.readlines()

    line_count = 0

    for line in line_list:
        line_count += 1
        input_url = line.split(',')[0]
        print(line_count, '/', len(line_list))
        # print('input_url: ' + input_url)
        get_search_result_urls(input_url)
