from urllib.parse import urljoin
from re import compile


def extract_generalatlantic_current(soup, main_url):
    urls = []
    row_divs = soup.find('div', {'data-pjax-container': ""}).findAll('div', {'class': 'row-fluid'})
    regx_href = compile("press-item")
    i = 0
    for div in row_divs:
        row = div.findAll('a', {'class': regx_href})
        if row:
            try:
                urls.append(urljoin(main_url, row[0].get('href')))
                urls.append(urljoin(main_url, row[1].get('href')))
                urls.append(urljoin(main_url, row[2].get('href')))
            except IndexError:
                pass
            i += 3

    return urls


def extract_generalatlantic_archive(soup, main_url):
    urls = []
    a_tags = soup.find('div', {'id': "press-archive-rows"}).findAll('a', {'class': 'archive-link'})
    i = 0
    for a_tag in a_tags:
        urls.append(urljoin(main_url, a_tag.get('href')))
        i += 1

    return urls
