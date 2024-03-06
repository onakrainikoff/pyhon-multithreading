import requests as http
import logging as log
from multiprocessing.pool import ThreadPool

urls = [
  'http://www.python.org',
  'https://docs.python.org/3/',
  'https://docs.python.org/3/whatsnew/3.7.html',
  'https://docs.python.org/3/tutorial/index.html',
  'https://docs.python.org/3/library/index.html',
  'https://docs.python.org/3/reference/index.html',
  'https://docs.python.org/3/using/index.html',
  'https://docs.python.org/3/howto/index.html',
  'https://docs.python.org/3/installing/index2.html',
  'https://docs.python.org/3/distributing/index2.html',
  'https://docs.python.org/3/extending/index2.html',
  'https://docs.python.org/3/c-api/index2.html',
  'https://docs.python.org/3/faq/index2.html'
  ]

log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)s [%(processName)s:%(threadName)s] - %(message)s")

def check_url(url):
    try:
        result = http.get(url, timeout=2)
        if result.ok:
            log.info(f"Result of of checking url={url} is ok")
        else:
            log.warning(f"Result of of checking url={url} is failed")
        return result.ok
    except Exception as error:
        log.error(f"Error of checking url={url}: {error}")
        return False

def check_urls_async(pool, urls):
    results = {}
    # check every url asyc
    for url in urls:
        result = pool.apply_async(check_url, [url])
        results[url] = result
    # wait completion of all checks
    for url, result in results.items():
        result.get()
    return results


if __name__ == "__main__":
    pool = ThreadPool(processes=5)
    try:
        results = check_urls_async(pool, urls)
        checks_list= ""
        for url, result in results.items():
            result.get()
            checks_list += f"\n\t{url} - is {'ok' if result.get() else 'failed'}"
        log.info(f"Results:{checks_list}")
    finally:
        pool.close()        