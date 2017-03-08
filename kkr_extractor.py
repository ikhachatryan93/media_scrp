from urllib.parse import urljoin


def extract_kkr(soup, main_url):
    urls = []
    div_tag = soup.find('div', {'class': "__blog-post-lists"})
    ul_tag = div_tag.find('ul', {'class': None})
    li_tags = ul_tag.findAll('li')
    i = 0
    for li in li_tags:
        i += 1
        url = li.contents[3].get('href')
        urls.append(urljoin(main_url, url))

    return urls
