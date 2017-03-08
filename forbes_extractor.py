from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup


def expected_date_is_reached(driver, end_date):
    dates = []
    try:
        dates = driver.find_elements_by_css_selector('.article-time.ng-binding')
    except Exception as e:
        print(str(e))
        exit(1)

    n = len(dates)
    if dates:
        if end_date in dates[n - 1].text:
            return True
        return False
    else:
        print("error: Could not extract dates from forbes")
        exit(1)


def scroll_until(driver, end_date="2014"):
    wait = WebDriverWait(driver, 10)

    while not expected_date_is_reached(driver, end_date):
        try:
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.load-more-search-button.fs-button')))
            element.click()

        except TimeoutException:
            break  # cannot click the button anymore
        except Exception as e:
            print(str(e))


def extract_urls(driver):
    soup = BeautifulSoup(driver.page_source, "html5lib")
    urls = []
    articles = soup.find("ul", {"class": "search-stream-results"}).findAll("li", {"class": "ng-scope"})
    for article in articles:
        a = article.find("a", {"class": "ng-scope"})
        url = a["href"]
        if url.startswith("//"):
            url = "http:" + url
        if url == "http://www.forbes.com/editors-picks/":
            continue
        urls.append(url)

    return urls


def extract_forbes(driver):
    scroll_until(driver, end_date="2014")
    return extract_urls(driver)
