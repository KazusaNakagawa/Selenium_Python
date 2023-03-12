import os
from dotenv import load_dotenv
from models.driver import (
    LoginSite,
    LoginSite2,
    YahooBrowser,
)

load_dotenv()


def yahoo_main():
    yb = YahooBrowser()
    queries = ['きょうの料理', 'ChatGTP おすすめ']
    try:
        for idx, query in enumerate(queries):
            if idx == 0:
                yb.search_query(by_class_name='_1wsoZ5fswvzAoNYvIJgrU4', query=query)
            else:
                yb.second_over_search_query(query=query)

    except Exception as ex:
        yb.log.logger.error(ex)
        yb.close()
    finally:
        yb.close()
        yb.log.logger.info('main end')


def login_site_main():
    url = os.environ['SITE_URL']
    email = os.environ['LOGIN_EMAIL']
    password = os.environ['LOGIN_PASSWORD']
    title = os.environ['ASSERT_TITLE']

    ls = LoginSite(url=url)
    try:
        ls.login(email=email, password=password, title=title)

    except Exception as ex:
        ls.log.logger.error(ex)
        ls.close()
    finally:
        ls.close()
        ls.log.logger.info('main end')


def login_site2_main():
    url = os.environ['SITE_URL2']
    company = os.environ['LOGIN_COMPANY_ID']
    email = os.environ['LOGIN_EMAIL2']
    password = os.environ['LOGIN_PASSWORD2']
    title = os.environ['LOGIN_TITLE2']

    ls2 = LoginSite2(url=url)
    try:
        ls2.login(company=company, email=email, password=password, login_title=title)

    except Exception as ex:
        ls2.log.logger.error(ex)
        ls2.close()
    finally:
        ls2.close()
        ls2.log.logger.info('main end')


if __name__ == '__main__':
    login_site2_main()
