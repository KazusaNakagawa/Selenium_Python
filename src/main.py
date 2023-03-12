from models.driver import YahooBrowser


def main():
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


if __name__ == '__main__':
    main()
