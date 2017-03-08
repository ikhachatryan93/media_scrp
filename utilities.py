from selenium import webdriver


def setup_phantomjs_browser(maximize=False):
    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any']
    phantomjs = webdriver.PhantomJS(service_args=service_args)
    if maximize:
        phantomjs.maximize_window()

    return phantomjs

def setup_edge_browser(maximize=False):
    edge = webdriver.Edge()
    if maximize:
        edge.maximize_window()

    return edge

def setup_chrome_browser(maximize=False):
    chrome = webdriver.Chrome("chromedriver.exe")  # , chrome_options=chrome_options)
    if maximize:
        chrome.maximize_window()

    return chrome


def write_urls_to_file(name, urls):
    with open(name, 'w', encoding='utf-8') as f:
        for url in urls:
            try:
                f.write(url + '\n')
            except Exception as e:
                print(str(e))
