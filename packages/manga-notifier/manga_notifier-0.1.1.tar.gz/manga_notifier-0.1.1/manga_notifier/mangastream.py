

import requests
from lxml import html

from meow import Meow

MANGASTREAM_URL = "http://www.mangastream.com"
MANGASTREAM_LIST_URL = "http://mangastream.com/manga"

def generate_html(url):
    response = requests.get(url)
    if response.ok:
        return response.content


def get_new_release(content):

    root = html.fromstring(content)

    for elem in root.xpath('//div[@class="side-nav hidden-xs"]/ul[@class="new-list"]/li'):
        for a in elem.xpath('./a'):
            name = a.xpath('text()')[0].strip()
            chapter = a.find('strong').text.strip()
            title = a.find('em').text.strip()
            url = a.attrib['href'].strip()

            yield (name, chapter, title, url)

def get_all_manga(content):

    root = html.fromstring(content)

def check_release(manga):

    content = generate_html(MANGASTREAM_URL)
    new = {}
    for k, v in manga.items():
        for release in get_new_release(content):
            if release[0] == k and int(release[1]) > int(v):
                Meow.meow("Chapter {} is OUT".format(release[1]), title=release[0], open=release[3])
                new[release[0]] = int(release[1])

    return new

if __name__ == "__main__":

    content = generate_html(MANGASTREAM_URL)

    for data in get_new_release(content):
        print("url=({})".format(data[3]))
