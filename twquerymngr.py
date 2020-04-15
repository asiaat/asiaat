from bs4 import BeautifulSoup
import datetime
from datetime import date, timedelta
from selenium import  webdriver
import time


class TWQueryMngr:
    # init method or constructor
    def __init__(self, search_url):
        self.search_url = search_url
        self.dates = []

        self.driver = webdriver.Chrome()
        self.search_words = []
        self.lang = 'en'

    def set_lang(self,_lang):
        self.lang = _lang

    def set_all_dates(self, start_date, end_date):

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        step = timedelta(days=1)
        while start_date <= end_date:
            self.dates.append(str(start_date.date()))
            start_date += step

    def scroll(self,_driver, start_date, end_date, words, lang, max_time=180):

        languages = {1: 'en', 2: 'it', 3: 'es', 4: 'fr', 5: 'de', 6: 'ru', 7: 'zh'}
        url = "https://twitter.com/search?q="
        for w in words[:-1]:
            url += "{}%20OR".format(w)
        url += "{}%20".format(words[-1])
        url += "since%3A{}%20until%3A{}&".format(start_date, end_date)
        if lang != 0:
            url += "l={}&".format(languages[lang])
        url += "src=typd"
        print(url)
        _driver.get(url)
        start_time = time.time()  # remember when we started
        while (time.time() - start_time) < max_time:
            _driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # print( str(time.time() - start_time) + " < " + str(max_time) )

    def scrape_tweets(self,_driver):

        try:
            tweet_divs = _driver.page_source
            obj = BeautifulSoup(tweet_divs, "html.parser")

            articles = obj.find_all("article")
            # print(articles)
            print(len(articles))

            for a in articles:

                try:
                    tw_text = a.find("div", {"lang": self.lang})

                    if tw_text != None:

                        tw_obj = BeautifulSoup(str(tw_text), "html.parser")
                        print(tw_obj.text)

                        tw_user = a.find("a", {"role": "link"})['href']
                        tw_datetime = a.find("time")['datetime']
                        print("user: " + tw_user)
                        print("tw datetime: " + tw_datetime)
                except:
                    print("Cannot read tweet")

        except Exception as e:
            print("Something went wrong!")
            print(e)
            driver.quit()


    def tw_search(self,_search_str):

        wordsToSearch = []
        wordsToSearch.append(_search_str)
        all_dates = self.dates
        # print(all_dates)

        for i in range(len(all_dates) - 1):
            driver = webdriver.Chrome()
            self.scroll(driver, str(all_dates[i]), str(all_dates[i + 1]), wordsToSearch, 1)
            self.scrape_tweets(driver)
            time.sleep(3)
            print("The tweets for {} are ready!".format(all_dates[i]))
            driver.quit()









