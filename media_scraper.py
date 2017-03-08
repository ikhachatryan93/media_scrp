#! /bin/env python

# modules from this projects
from utilities import write_urls_to_file
from utilities import setup_phantomjs_browser
from utilities import setup_chrome_browser
from generalatlantic_extractor import extract_generalatlantic_current, extract_generalatlantic_archive
from kkr_extractor import extract_kkr
from forbes_extractor import extract_forbes
from nytimes_extractor import extract_nytimes

# standard modules
from urllib.request import urlopen
from contextlib import closing
import time

# third party modules
from bs4 import BeautifulSoup

media_kkr_url = "http://media.kkr.com/media/media_releases.cfm?NumberPerPage=10000&Year=&ReleasesType=KKR+in+the+News" \
                "&SortOrder=Date+Descending "
media_kkr_main_url = "http://media.kkr.com/media/"

gen_at_url_current = "http://www.generalatlantic.com/media/general-atlantic/"
gen_at_url_archive = "http://www.generalatlantic.com/media/archive/"
gen_at_url_main = "http://www.generalatlantic.com"

forbes_url = "https://www.forbes.com/search/?q=%22private%20equity%22&sort=date"

nytimes_urls = ['''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20140101to20140630'''
    , '''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20140701to20141231'''
    , '''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20150101to20150630'''
    , '''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20150701to20151231'''
    , '''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20160101to20160630'''
    , '''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20160701to20161231'''
    , '''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20170101to20170630'''
    , '''https://query.nytimes.com/search/sitesearch/?action=click&contentCollection%C2%AEion=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/%22private+equity/from20170701to20171231''']

nytimes_url_main = '''https://www.nytimes.com/'''


def extract(url, main_url="", urllib_based=None, selenium_based=None):
    print("Extracting {}".format(main_url))
    urls = []
    #try:

    if selenium_based is not None:
        driver = setup_chrome_browser(maximize=True)
        #driver = setup_phantomjs_browser(maximize=True)
        driver.get(url)
        time.sleep(1)
        driver.get(url)
        urls = selenium_based(driver)
        driver.quit()
    else:
        print(url)
        with closing(urlopen(url)) as html:
            soup = BeautifulSoup(html.read(), "lxml")
            urls = urllib_based(soup, main_url)

    #except Exception as e:
    #    print(str(e))
    print("Extracted urls: {}".format(len(urls)))

    return urls


def main():
    gen_urls = extract(gen_at_url_archive, gen_at_url_main, urllib_based=extract_generalatlantic_archive)
    gen_urls += extract(gen_at_url_current, gen_at_url_main, urllib_based=extract_generalatlantic_current)
    write_urls_to_file("general_atlantic_urls.txt", gen_urls)

    # kkr_urls = extract(media_kkr_url, media_kkr_main_url, urllib_based=extract_kkr)
    # write_urls_to_file("kkr_urls.txt", kkr_urls)

    # forbes_urls = extract(forbes_url, "forbes.com", selenium_based=extract_forbes)
    # write_urls_to_file("forbs_urls.txt", forbes_urls)

    # nytimes_articles = extract_nytimes(nytimes_urls)
    # write_urls_to_file("nytimes_urls.txt", nytimes_articles)

    # write_urls_to_file("all_urls.txt", kkr_urls + gen_urls + forbes_urls + nytimes_articles)

if __name__ == "__main__":
    main()
