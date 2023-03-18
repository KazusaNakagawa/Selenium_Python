"""
Main executable file.
"""
import json
import sys
from time import sleep
from models.driver import (
    Driver,
    YahooBrowser,
)


def yahoo_main():
    """Crawl Yahoo Engine"""
    yahoo_engine = YahooBrowser()
    queries = ['きょうの料理', 'ChatGTP おすすめ']
    try:
        for idx, query in enumerate(queries):
            if idx == 0:
                yahoo_engine.search_query(by_class_name='_1wsoZ5fswvzAoNYvIJgrU4', query=query)
            else:
                yahoo_engine.second_over_search_query(query=query)

    except Exception as ex:
        yahoo_engine.log.logger.error(ex)
    finally:
        yahoo_engine.close()
        yahoo_engine.log.logger.info('main end')


def main():
    """
    invocation parameter:
      sys.argv[2]: crawl.json target ID
      sys.argv[4]: headdless mode: { 0: False, 1: True }

    ex:
      python main.py --target id0002 --headless 1
      python main.py --target id0001 --headless 0
    """
    with open('./conf/crawl.json', 'r') as json_file:
        json_crawl = json.load(json_file)
        target_id = json_crawl[0][sys.argv[2]]
        site = target_id['site']
        account = target_id['account']
        xpath = site['xpath']

    driver = Driver(url=site['url'], headless=int(sys.argv[4]))

    try:
        driver.assert_title_check(title=site['login_title'])
        if xpath['company']:
            driver.send_key(xpath=xpath['company'], send_key=account['company'])
        driver.send_key(xpath=xpath['email'], send_key=account['email'])
        driver.send_key(xpath=xpath['password'], send_key=account['password'])
        driver.click_bottom(xpath=xpath['loginButton'])
        sleep(5)
        driver.assert_title_check(title=site['home_title'])

    except Exception as ex:
        driver.log.logger.error(ex)
    finally:
        driver.close()
        driver.log.logger.info('main end')


if __name__ == '__main__':
    main()
