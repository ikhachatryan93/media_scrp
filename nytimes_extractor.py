from urllib.request import urlopen
from contextlib import closing
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities import setup_phantomjs_browser
from utilities import setup_chrome_browser

import sys
import time


def extract_urls(url, articles):
    driver = setup_phantomjs_browser()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    while True:
        try:
            page_articles = wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, '.element2>h3>a')))
        except Exception as e:
            print("Exception 1 : {}".format(str(e)))
            driver.quit()
            break
        for p in page_articles:
            art = p.get_attribute("href")
            articles.append(art)
            print(art)
        try:
            next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".stepToPage.next")))
        except:
            driver.quit()
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_page.click()
    print(len(articles))


def extract_nytimes(urls, threads_num=4):
    i = 0
    total = len(urls)
    trds = []
    articles = []
    for url in urls:
        i += 1
        sys.stdout.write("\r[Extracting: {}/{}]".format(i, total))
        sys.stdout.flush()
        time.sleep(0.3)
        t = threading.Thread(target=extract_urls, args=(url, articles))
        t.daemon = True
        t.start()
        trds.append(t)
        while threading.active_count() > threads_num:
            time.sleep(0.4)
    for i in trds:
        i.join(10)
    return articles
