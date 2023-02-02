import json
import time
import requests
import random
import threading
import itertools
import urllib.parse
from urllib.parse import urlencode
from user_agents import parse
from argparse import ArgumentParser
from termcolor import colored
import colorama
colorama.init()


def get_arg_parser():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-t", "--thread", default=2,
                            type=int, help="Threads")
    arg_parser.add_argument("-t1", "--time1", default=5,
                            type=int, help="Time in seconds")
    arg_parser.add_argument("-t2", "--time2", default=10,
                            type=int, help="Time in seconds")
    return arg_parser


def get_proxies_from_file(file_path):
    with open(file_path, 'r') as f:
        return [l.strip() for l in f]


def get_next_proxy(proxies):
    for proxy in itertools.cycle(proxies):
        yield proxy


def get_user_agents_from_file(file_path):
    with open(file_path, 'r') as f:
        return [l.strip() for l in f]


def get_next_user_agent(user_agents):
    for user_agent in itertools.cycle(user_agents):
        yield user_agent


def get_ads_from_file(file_path):
    with open(file_path, 'r') as f:
        return [l.strip().split(',') for l in f]


def get_random_url_ad(ads):
    url_ad = random.choice(ads)
    return f"https://apis.adsalo.com/v2/ca/ads?client={url_ad[0]}&slot={url_ad[1]}&ref={url_ad[2]}"


def get_impression(url_ad, proxy, headers):
    proxies = None
    if proxy != 'L':
        if proxy.startswith('socks4'):
            proxies = {'http': f'{proxy}',
                       'https': f'{proxy}'}
        elif proxy.startswith('socks'):
            proxies = {'http': f'{proxy}',
                       'https': f'{proxy}'}
        else:
            proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}

    try:
        response = requests.get(
            url_ad, allow_redirects=True, timeout=30, headers=headers, proxies=proxies, verify=True)
        if response.status_code == 200:
            data = response.text
            if data != '':
                impress = json.loads(data)
                parsed = urllib.parse.urlparse(url_ad)
                query = urllib.parse.parse_qs(parsed.query)
                client = query.get("client", [None])[0]

                return (True, f"https://apis.adsalo.com/v2/ca/ads?client={client}&site={impress['data']['siteUrl']}")
            else:
                return (False, False)
    except:
        return (False, False)


def get_click(impress, proxy, headers):
    if impress:
        proxies = None
        if proxy != 'L':
            if proxy.startswith('socks4'):
                proxies = {'http': f'{proxy}',
                           'https': f'{proxy}'}
            elif proxy.startswith('socks'):
                proxies = {'http': f'{proxy}',
                           'https': f'{proxy}'}
            else:
                proxies = {'http': f'http://{proxy}',
                           'https': f'https://{proxy}'}

        try:
            response = requests.get(
                impress, allow_redirects=True, timeout=30, headers=headers, proxies=proxies, verify=True)
            if response.status_code == 200:
                return (True, True)
        except:
            return (False, False)
    else:
        return (False, False)


def get_ipv4(impress, proxy, user_agent):
    if impress:
        headers = {'User-Agent': user_agent}
        proxies = None
        if proxy != 'L':
            if proxy.startswith('socks4'):
                proxies = {'http': f'{proxy}',
                           'https': f'{proxy}'}
            elif proxy.startswith('socks'):
                proxies = {'http': f'{proxy}',
                           'https': f'{proxy}'}
            else:
                proxies = {'http': f'http://{proxy}',
                           'https': f'https://{proxy}'}

        try:
            response = requests.get(
                "http://checkip.amazonaws.com", allow_redirects=True, timeout=30, headers=headers, proxies=proxies, verify=False)
            if response.status_code == 200:
                return (True, response.text.strip())
        except:
            return (False, False)
    else:
        return (False, False)


def print_color(value):
    if value == True:
        return (colored("True", "green"))
    elif value == False:
        return (colored("False", "red"))
    else:
        return value


def get_language():
    languages = ['en-US', 'en', 'fr', 'de',
                 'zh-CN', 'ja', 'es', 'ru', 'pt-BR', 'id']
    num_languages = int(random.uniform(1, 4))

    accept_languages = random.sample(languages, num_languages)
    accept_languages_header = ", ".join(
        [lang + ";q=" + str(round(random.uniform(0.7, 1), 1)) for lang in accept_languages])
    return accept_languages_header


def main(proxies, user_agents, ads, argss):
    while True:
        proxy = next(proxies)
        user_agent = next(user_agents)
        language = get_language()
        parsed_ua = parse(user_agent)
        url_ad = get_random_url_ad(ads)

        headers_impress = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": language,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Ch-Ua": f"\"{parsed_ua.browser.family}\";v=\"{parsed_ua.browser.version_string}\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": parsed_ua.os.family,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Referer": "https://allinsaja.blogspot.com/",
        }
        headers_click = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": language,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Ch-Ua": f"\"{parsed_ua.browser.family}\";v=\"{parsed_ua.browser.version_string}\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": parsed_ua.os.family,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Referer": "https://allinsaja.blogspot.com/",
        }

        impress = get_impression(url_ad, proxy, headers_impress)
        ipv4 = get_ipv4(impress[1], proxy, user_agent)
        if impress[0] == True:
            time.sleep(int(random.uniform(1, 5)))
        click = get_click(impress[1], proxy, headers_click)
        time.sleep(int(random.uniform(1, 5)))

        if impress is None:
            impress = [False, False]
        if click is None:
            click = [False, False]
        if ipv4 is None:
            ipv4 = [False, False]

        print("Impression " + print_color(impress[0]) +
              " | Click " + print_color(click[0])+" | IP "+print_color(ipv4[1]))
        time.sleep(int(random.uniform(argss.time1, argss.time2)))


if __name__ == '__main__':
    arg_parser = get_arg_parser()
    argss = arg_parser.parse_args()

    proxies = get_proxies_from_file('p.txt')
    user_agents = get_user_agents_from_file('ua.txt')
    ads = get_ads_from_file('ads.txt')
    random.shuffle(proxies)
    random.shuffle(user_agents)
    random.shuffle(ads)
    proxies = get_next_proxy(proxies)
    user_agents = get_next_user_agent(user_agents)

    threads = []

    for i in range(argss.thread):
        t = threading.Thread(target=main, args=(
            proxies, user_agents, ads, argss))
        threads.append(t)
        t.start()
    for th in threads:
        th.join()
