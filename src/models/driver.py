import os
import sys
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from models.org_log import Log

_EXEC_FILE_NAME = os.path.basename(__file__)[:-3]


class NoneElementsError(Exception):
    """ None Elements Error """


class Driver(object):

    def __init__(self, url="https://www.google.co.jp/"):
        """Default: Google Chrome
          params:
            url(str): search target url
        """
        self.log = Log(logger_name=_EXEC_FILE_NAME)
        self.log.logger.info('init ...')
        options = Options()
        options.add_argument('--window-size=640,1024')

        if len(sys.argv) > 1 and sys.argv[1] == '--linux':
            # docker, linux etc
            options.binary_location = '/usr/bin/google-chrome'
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('disable-application-cache')
            chrome_service = service.Service(executable_path='/usr/bin/chromedriver')
            self.driver = webdriver.Chrome(service=chrome_service, options=options)
        else:
            # local Mac M1: 10.0.5481.177（Official Build） （arm64）
            chrome_service = service.Service(executable_path='/usr/local/bin/chromedriver')
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            # options.add_argument('disable-application-cache')
            # options.add_argument('--user-data-dir=/path/to/cache/directory')
            self.driver = webdriver.Chrome(service=chrome_service, options=options)
            # self.driver = webdriver.Chrome(options=options)

        self.wait = WebDriverWait(self.driver, 10)
        # search url
        self.driver.get(url)
        self.log.logger.info({'url': url})
        self.log.logger.info('init end')

    def close(self):
        self.driver.close()
        self.driver.quit()
        self.log.logger.info('done')

    def search_query(self, by_class_name='gLFyf', query=None, sleep_=5) -> None:
        """ 指定文字列で検索し Enter

        params:
          by_class_name(str): 検索タグのクラス名, default: gLFyf (Google)
          query(str)     : 検索文字列, default: None
          sleep_(int)    : 処理間隔 (sec)
        """

        try:
            elements = self.wait.until(lambda x: x.find_elements(By.CLASS_NAME, by_class_name))
            self.log.logger.debug({f"elements: {elements}"})

            if not elements:
                raise NoneElementsError

            if query:
                event = {"element": elements[0]}
                self.log.logger.info(f"search query: {query}")
                event["element"].send_keys(query)
                event["element"].send_keys(Keys.ENTER)
                self.driver.implicitly_wait(20)
                # 入力値 clear
                self.clear_search_box()

        except NoneElementsError:
            self.log.logger.error('None elements Error ...')
            self.close()
        except Exception as ex:
            self.log.logger.error({f"'ex: '{ex}"})
            self.log.logger.error(traceback.format_exc())
            self.close()

    def login(self, *args, **keywords) -> None:
        pass

    def second_over_search_query(self, *args, **keywords) -> None:
        pass

    def clear_search_box(self, *args, **keywords) -> None:
        pass


class YahooBrowser(Driver):

    def __init__(self, url='https://www.yahoo.co.jp'):
        super().__init__(url=url)

    def second_over_search_query(self, by_class_name='SearchBox__searchInput', query=None, sleep_=3) -> None:
        """ 検索文字列入力 2回目以降 """
        elements = self.wait.until(lambda x: x.find_elements(By.CLASS_NAME, by_class_name))

        event = {"element": elements[0]}
        self.log.logger.info(f"search query: {query}")
        event["element"].send_keys(query)
        event["element"].send_keys(Keys.ENTER)
        sleep(sleep_)
        self.clear_search_box()

    def clear_search_box(self, by_class_name='SearchBox__clearButton', sleep_=3) -> None:
        """ 検索文字列を削除 """
        elements = self.driver.find_elements(By.CLASS_NAME, by_class_name)
        event = {"element": elements[0]}
        self.log.logger.debug({f"elements: {elements}"})
        event["element"].send_keys(Keys.ENTER)
        self.log.logger.info({f"msg: cleared search box"})

        sleep(sleep_)


class LoginSite(Driver):
    def __init__(self, url=None):
        super().__init__(url=url)

    def login(self, email, password, title, login_title):

        assert self.driver.title == login_title
        self.log.logger.info({'msg': f"{login_title} OK"})

        elements = self.wait.until(lambda x: x.find_elements(By.XPATH, '//*[@id="email"]'))
        event = {"element": elements[0]}
        event["element"].send_keys(email)

        elements = self.wait.until(lambda x: x.find_elements(By.XPATH, '//*[@id="password"]'))
        event = {"element": elements[0]}
        event["element"].send_keys(password)

        try:
            elements = self.wait.until(lambda x: x.find_elements(By.XPATH, '//*[@id="login-form"]/div[3]/button'))
            # headless mode: login button が なくなる ...
            self.driver.execute_script("arguments[0].click();", elements[0])
            sleep(5)

            # assert self.driver.title == title
            # self.log.logger.info({'msg': f"{title} OK"})
            elements = self.wait.until(
                lambda x: x.find_elements(
                    By.XPATH,
                    '//*[@id="main-content"]/div/div/div[2]/form/div[2]/div[1]/div[1]/div[1]'))
            sleep(5)
            assert elements[0].text == '年収・給与'

        except Exception as ex:
            self.log.logger.error({
                'ex': ex,
                'trace': traceback.format_exc(),
                'current_title': self.driver.title,
            })
            # Error した時の html ファイルを書き込む
            with open(f"../log/{self.driver.title}_source.html", 'w', encoding='UTF-8') as f:
                f.write(self.driver.page_source)


class LoginSite2(Driver):
    def __init__(self, url=None):
        super().__init__(url=url)

    def login(self, company, email, password, login_title):
        assert self.driver.title == login_title
        self.log.logger.info({'msg': f"{login_title} OK"})

        elements = self.wait.until(
            lambda x: x.find_elements(By.XPATH, '//*[@id="employee_session_form_office_account_name"]'))
        event = {"element": elements[0]}
        event["element"].send_keys(company)

        elements = self.wait.until(
            lambda x: x.find_elements(By.XPATH, '//*[@id="employee_session_form_account_name_or_email"]'))
        event = {"element": elements[0]}
        event["element"].send_keys(email)

        elements = self.wait.until(
            lambda x: x.find_elements(By.XPATH, '//*[@id="employee_session_form_password"]'))
        event = {"element": elements[0]}
        event["element"].send_keys(password)

        elements = self.wait.until(
            lambda x: x.find_elements(
                By.XPATH, '/html/body/div[1]/div/div/div/div/form/div[4]/input'))
        sleep(3)
        self.driver.execute_script("arguments[0].click();", elements[0])

        home_title = 'ホーム | マネーフォワード クラウド勤怠'
        assert self.driver.title == home_title
        self.log.logger.info({'msg': f"{home_title} OK"})
