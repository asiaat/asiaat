from bs4 import BeautifulSoup
import datetime
from datetime import date, timedelta
from selenium import  webdriver
import time


class TWQueryMngr:
    # init method or constructor
    def __init__(self):
        self.search_url = "https://twitter.com/search?q="
        self.dates      = []

        self.driver         = webdriver.Chrome()
        self.search_words   = []
        self.lang           = 'en'
        self.output         = None

    def set_driver(self,_driver):
        self.driver = _driver

    def set_lang(self,_lang):
        self.lang = _lang

    def set_all_dates(self, start_date, end_date):

        start_date  = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date    = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        step = timedelta(days=1)
        while start_date <= end_date:
            self.dates.append(str(start_date.date()))
            start_date += step

    def scroll(self, start_date, end_date, words, lang, max_time=180):

        languages = {1: 'en', 2: 'it', 3: 'es', 4: 'fr', 5: 'de', 6: 'ru', 7: 'zh'}
        url = self.search_url
        for w in words[:-1]:
            url += "{}%20OR".format(w)
        url += "{}%20".format(words[-1])
        url += "since%3A{}%20until%3A{}&".format(start_date, end_date)
        if lang != 0:
            url += "l={}&".format(languages[lang])
        url += "src=typd"
        print(url)
        self.driver.get(url)
        start_time = time.time()  # remember when we started
        while (time.time() - start_time) < max_time:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scrape_tweets(self):

        try:

            obj = BeautifulSoup(self.driver.page_source, "html.parser")

            for a in obj.find_all("article"):

                try:
                    tw_text = a.find("div", {"lang": self.lang})

                    if tw_text != None:

                        tw_obj      = BeautifulSoup(str(tw_text), "html.parser")
                        tw_user     = a.find("a", {"role": "link"})['href'].strip("/")
                        tw_datetime = a.find("time")['datetime']

                        json_entry = {
                            "tweet":tw_obj.text,
                            "user":tw_user,
                            "timestamp":tw_datetime
                        }

                        print (json_entry)
                        self.output.write(str(json_entry)+"\n")

                except:
                    print("Cannot read tweet")

        except Exception as e:
            print("Something went wrong!")
            print(e)


    def tw_search(self,_search_str):

        wordsToSearch = []
        wordsToSearch.append(_search_str)
        all_dates   = self.dates
        self.output = open("output.json","w")

        for i in range(len(all_dates) - 1):
            self.driver = webdriver.Chrome()
            self.scroll(str(all_dates[i]), str(all_dates[i + 1]), wordsToSearch, 1)
            self.scrape_tweets()
            time.sleep(3)
            print("The tweets for {} are ready!".format(all_dates[i]))
            self.driver.quit()

        self.output.close()







