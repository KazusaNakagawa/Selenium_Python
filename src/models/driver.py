import os
import sys
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from src.models.org_log import Log

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
        options.add_argument('--window-size=1280,1024')

        if len(sys.argv) > 1 and sys.argv[1] == '--linux':
            # docker, linux etc
            options.binary_location = '/usr/bin/google-chrome'
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-gpu")
            chrome_service = service.Service(executable_path='/usr/bin/chromedriver')
            self.driver = webdriver.Chrome(service=chrome_service, options=options)
        else:
            chrome_service = service.Service(executable_path='/usr/local/bin/chromedriver')
            self.driver = webdriver.Chrome(service=chrome_service, options=options)
        # search url
        self.driver.get(url)
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
            elements = self.driver.find_elements(By.CLASS_NAME, by_class_name)
            self.log.logger.debug({f"elements: {elements}"})

            if not elements:
                raise NoneElementsError

            if query:
                event = {"element": elements[0]}
                self.log.logger.info(f"search query: {query}")
                event["element"].send_keys(query)
                event["element"].send_keys(Keys.ENTER)
                sleep(sleep_)

        except NoneElementsError:
            self.log.logger.error('None elements Error ...')
        except Exception as ex:
            self.log.logger.error({f"'ex: '{ex}"})
            self.log.logger.error(traceback.format_exc())
        finally:
            self.close()
