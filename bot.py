import json
import time
import requests
import random
import threading
from argparse import ArgumentParser


USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; J8110 Build/55.0.A.0.552; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; HTC Desire 21 pro 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
    "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
]

PROXIES = [
    "grjzwrki:md4guryfe6de@185.199.229.156:7492",
    "grjzwrki:md4guryfe6de@185.199.228.220:7300",
    "grjzwrki:md4guryfe6de@185.199.231.45:8382",
    "grjzwrki:md4guryfe6de@188.74.210.207:6286",
    "grjzwrki:md4guryfe6de@188.74.183.10:8279",
    "grjzwrki:md4guryfe6de@188.74.210.21:6100",
    "grjzwrki:md4guryfe6de@45.155.68.129:8133",
    "grjzwrki:md4guryfe6de@154.95.36.199:6893",
    "grjzwrki:md4guryfe6de@45.94.47.66:8110",
    "grjzwrki:md4guryfe6de@144.168.217.88:8780",
]

URL_ADS = [
    ['ca-pub-udmnpq-00000000008', 'y4da1k7c1k', 'sidebar1'],
    ['ca-pub-gojwcs-00000000009', '7xxm991zmc', 'post'],
    ['ca-pub-byosny-00000000052', '1w41ct9ugr', 'sidebar2'],
    ['ca-pub-ehbqgq-00000000053', 'vtf6zy5j3n', 'header'],
    ['ca-pub-sepngh-00000000054', '1q5236304i', 'home'],
    ['ca-pub-vdcolm-00000000065', 'u4w8be84r5', 'footer1'],
    ['ca-pub-jlgdyn-00000000068', 'jf27ky091w', 'footer2'],
    ['ca-pub-wiljai-00000000069', '8p4l78dirp', 'footer3'],
    ['ca-pub-vdkezq-00000000070', 'cxw43u0366', 'sidebar3'],
    ['ca-pub-ijtjbf-00000000071', '8a7562x81p', 'sidebar4'],
    ['ca-pub-hbvjqf-00000000157', '7z9l743467', 'sidebar5'],
    ['ca-pub-dsqnab-00000000158', '75fy1icfw7', 'sidebar6'],
    ['ca-pub-dsqnab-00000000158', '75fy1icfw7', 'sidebar6'],
    ['ca-pub-qmhidd-00000000159', '89wo4zx90y', 'sidebar7'],
    ['ca-pub-bqipqu-00000000160', '0793ce03tr', 'sidebar8'],
    ['ca-pub-mjyqkg-00000000161', 'qn3jm12kj8', 'home1'],
]


def get_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-t", "--thread", default=4,
                            type=int, help="Threads")
    arg_parser.add_argument(
        "-p",
        "--proxy",
        help="ip:port or username:password@host:port",
    )
    return arg_parser


def get_random_user_agent() -> str:
    user_agent = random.choice(USER_AGENTS)
    return user_agent


def get_random_proxy() -> str:
    proxy = random.choice(PROXIES)
    return proxy


def get_random_url_ad() -> str:
    url_ad = random.choice(URL_ADS)
    return url_ad


def getImpress(url, user_agent, proxy):
    if proxy != 'L':
        proxies = {
            "http": "socks5://"+proxy+"/",
            "https": "socks5://"+proxy+"/"
        }
    else:
        proxies = False

    r = requests.get(url, allow_redirects=True, timeout=30, headers={
                     'User-Agent': user_agent}, proxies=proxies)
    return r


def main():
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    while True:
        user_agent = get_random_user_agent()
        if args.proxy == 'O':
            proxy = get_random_proxy()
        else:
            proxy = 'L'

        url_ad = get_random_url_ad()
        url = f"https://apis.adsalo.com/v2/ca/ads?client={url_ad[0]}&slot={url_ad[1]}&ref=allinsaja.blogspot.com"
        r = getImpress(url, user_agent, proxy)
        
        # url_p = "https://ipv4.webshare.io"
        # r_p = getImpress(url_p, user_agent, proxy).text
        # msg_ad = f"{r_p} || {url_ad[2]}"

        msg_ad = f"{url_ad[2]}"
        msg_o = f"{'O' if proxy != 'L' else 'L'} | "

        if (r.status_code == 200):
            data = r.text
            if data != '':
                jsonD = json.loads(data)
            else:
                jsonD = 0
        else:
            jsonD = 0

        resp = jsonD

        if resp != 0:
            urlAd = f"https://apis.adsalo.com/v2/ca/ads?client={url_ad[0]}&site={resp['data']['siteUrl']}"

            try:
                click = getImpress(urlAd, user_agent, proxy).status_code
                msg_o += f"Success {click} | {msg_ad}"
            except:
                msg_o += f"Failed | {msg_ad}"
        else:
            msg_o += f"Failed to impress | {msg_ad}"

        print(msg_o)
        time.sleep(2)


if __name__ == '__main__':
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    threads = []
    for th in range(args.thread):
        t = threading.Thread(target=main)
        threads.append(t)
        t.start()
    for thh in threads:
        thh.join()
