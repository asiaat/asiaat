from twquerymngr import TWQueryMngr


if __name__ == '__main__':

    tw_search_url   =  "https://twitter.com/search?q="

    tq = TWQueryMngr(tw_search_url)

    tq.set_all_dates("2020-04-04","2020-04-06")
    tq.tw_search("graffiti")