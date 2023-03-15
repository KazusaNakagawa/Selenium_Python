## Selenium Python

### premise
* Mac M1
* Python: 3.10.x

### Procedure
1. [Create a temporary environment.](https://docs.python.org/3/library/venv.html#module-venv)
   ```bash
   python3 -m venv venv
   ```
2. activate venv
   ```bash
   source venv/bin/activate
   ```
3. Install the package
   ```bash
   pip install -r requirements.txt
   ```
4. set `crawl.json`

   Please refer to [crawl.json.sample](https://github.com/KazusaNakagawa/selenium-python/blob/develop/src/conf/crawl.json.sample) to set the value to be crawled.

5. Run `main.py`.
   ```bash
   # cd src/
   ex:
   python main.py --target id0002 --headless 1
   ```

### Docker
**Consideration.**

I have the chromedriver and google chrome versions matched, but it does not work on v110.0.5481 series.

## Ref
* [logging.handlers Timedrotatingfilehandler](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler)
* https://selenium-python.readthedocs.io/
* [nightmare or Selenium 環境構築](https://kazusabook.notion.site/nightmare-or-Selenium-a8330ccfdc95433d8b2e72293eddcdd6) 
