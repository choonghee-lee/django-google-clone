from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import requests

from .models import Site, Image


class DomDocumentParser:
    """
    html 파서

    url을 입력하면 필요한 내용을 파싱해준다.
    """

    def get_links(self, url, href=''):
        links = []
        response = requests.get(url, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        bs = BeautifulSoup(response.content, 'html.parser')
        all_links = bs.find_all('a', href=re.compile(href))
        for link in all_links:
            links.append(link.attrs['href'])
        return links

    def get_title_tags(self, url):
        response = requests.get(url, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        bs = BeautifulSoup(response.content, 'html.parser')
        return bs.find_all('title')

    def get_meta_tags(self, url):
        response = requests.get(url, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        bs = BeautifulSoup(response.content, 'html.parser')
        return bs.find_all('meta')

    def get_images(self, url):
        response = requests.get(url, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        bs = BeautifulSoup(response.content, 'html.parser')
        return bs.find_all('img')


crawled = []
crawling = []
found_images = []


def insert_link(url, title, description, keywords):
    """
    데이터베이스에 사이트 정보 저장
    """

    # 중복 불가능
    if Site.objects.filter(url=url).exists():
        return

    site = Site()
    site.url = url
    site.title = title
    site.description = description
    site.keyword = keywords
    site.save()


def insert_image(url, src, title, alt):
    """
    데이터베이스에 이미지 정보 저장
    """
    if Image.objects.filter(image_url=src).exists():
        return

    image = Image()
    image.site_url = url
    image.image_url = src
    image.title = title
    image.alt = alt

    image.save()


def create_link(url, href):
    """
    relative url을 absolute url로 변경

    ex)
    //hello.com/ => http://hello.com/
    """
    src = href
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    host = parsed_url.netloc
    path = parsed_url.path

    if src[:2] == "//":
        src = scheme + ":" + src
    elif src[:1] == "/":
        src = scheme + "://" + host + src
    elif src[:2] == './':
        src = scheme + "://" + host + path + src[1:]
    elif src[:3] == '../':
        src = scheme + "://" + host + "/" + src
    elif src[:5] != "https" and src[:4] != "http":
        src = scheme + "://" + host + "/" + src
    return src


def get_details(url):
    """
    url에 해당하는 웹페이지의 상세 정보를 찾아서
    데이터베이스에 저장한다.
    """
    global found_images

    parser = DomDocumentParser()
    titles = parser.get_title_tags(url)
    if titles == False:
        return

    title = titles[0].text
    title = title.replace("\n", "")
    if title == "":
        return

    description = ""
    keywords = ""
    metas = parser.get_meta_tags(url)
    for meta in metas:
        try:
            if meta.attrs['name'] == "description":
                description = meta.attrs['content']

            if meta.attrs['name'] == "keywords":
                keywords = meta.attrs['content']
        except KeyError:
            pass

    description = description.replace("\n", "")
    keywords = keywords.replace("\n", "")

    insert_link(url, title, description, keywords)
    print("SITE:", url)

    src = ""
    title = ""
    alt = ""
    images = parser.get_images(url)
    for image in images:
        try:
            src = image.attrs['src']
            title = image.attrs['title']
            alt = image.attrs['alt']

            src = create_link(url, src)
            print(src)

            if src not in found_images:
                found_images.append(src)

                # Insert the image
                insert_image(url, src, title, alt)
                print("Image:", src)
        except KeyError:
            pass


def crawl_links(url, links):
    """
    웹 크롤링

    href를 통해 계속 크롤링한다.
    거의 무한루프 상태에 빠지며, 서버에서 리커넥션을 할 것이다 ㅋㅋ..
    """
    global crawled
    global crawling

    refined_links = []
    for href in links:
        if '#' in href:
            continue
        elif 'javascript:' in href:
            continue

        href = create_link(url, href)

        if href not in crawled:
            crawled.append(href)
            crawling.append(href)

            # Insert href
            get_details(href)

        refined_links.append(href)

    crawling.pop(0)

    for site in crawling:
        crawl_links(site)

    return refined_links
