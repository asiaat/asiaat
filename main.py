from twquerymngr import TWQueryMngr


if __name__ == '__main__':

    tq = TWQueryMngr()
    tq.set_all_dates("2020-04-04","2020-04-05")
    tq.tw_search("graffiti")