from src.models.driver import Driver

if __name__ == '__main__':
    d = Driver(url='https://www.yahoo.co.jp/')
    d.search_query(by_class_name='_1wsoZ5fswvzAoNYvIJgrU4', query='きょうの料理')