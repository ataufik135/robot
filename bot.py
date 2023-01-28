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
    "L"
    "157.245.247.84:59166",
    "164.163.32.3:59166",
    "128.199.212.124:59166",
    "46.101.37.189:59166",
    "45.33.21.96:64913",
    "174.138.33.62:59166",
    "96.126.113.216:59166",
    "159.89.228.253:38172",
    "157.230.19.132:59166",
    "45.118.144.113:59166",
    "106.52.104.55:59166",
    "159.203.13.82:59166",
    "192.111.135.18:18301",
    "67.201.33.10:25283",
    "47.242.87.234:9527",
    "103.70.79.28:59166",
    "138.197.203.84:59166",
    "98.142.110.251:59166",
    "192.252.216.81:4145",
    "51.178.82.49:59166",
    "51.255.95.41:59166",
    "174.64.199.82:4145",
    "128.199.228.54:59166",
    "169.56.21.196:1080",
    "141.95.103.206:1234",
    "125.143.142.204:1080",
    "66.42.224.229:41679",
    "174.64.199.79:4145",
    "159.89.34.109:59166",
    "178.128.212.72:59166",
    "157.230.39.148:59166",
    "138.197.185.192:59166",
    "192.252.208.70:14282",
    "64.225.6.88:59166",
    "94.182.190.241:1080",
    "172.104.173.122:59166",
    "142.54.226.214:4145",
    "89.179.126.189:1080",
    "72.37.217.3:4145",
    "51.255.219.244:59166",
    "142.54.236.97:4145",
    "68.183.55.211:37775",
    "192.241.149.84:17999",
    "159.89.49.172:59166",
    "149.202.69.31:1080",
    "206.189.112.62:59166",
    "45.158.230.159:24109",
    "159.65.220.89:59166",
    "162.55.95.166:8888",
    "173.249.28.60:59166",
    "104.248.158.27:25100",
    "158.69.225.110:59166",
    "118.171.168.165:50862",
    "165.227.153.96:59166",
    "103.196.136.158:59166",
    "142.54.232.6:4145",
    "68.71.249.153:48606",
    "68.71.254.6:4145",
    "104.237.134.201:59166",
    "188.93.213.242:1080",
    "65.169.38.73:26592",
    "142.93.250.71:59166",
    "170.210.156.33:59166",
    "178.62.202.227:59166",
    "68.71.247.130:4145",
    "51.158.124.186:59166",
    "129.146.242.19:2049",
    "152.228.171.118:59166",
    "142.54.237.34:4145",
    "172.104.210.40:59166",
    "88.151.99.173:33980",
    "74.119.147.209:4145",
    "199.229.254.129:4145",
    "192.111.137.34:18765",
    "72.37.216.68:4145",
    "51.68.125.26:59166",
    "128.199.143.141:59166",
    "165.22.52.169:17171",
    "8.142.3.145:3306",
    "51.79.251.116:59166",
    "139.59.193.106:59166",
    "5.189.179.173:59166",
    "51.195.116.88:1234",
    "134.209.99.92:59166",
    "165.227.187.48:59166",
    "178.128.117.95:59166",
    "128.199.120.36:59166",
    "192.111.130.2:4145",
    "5.130.185.31:10801",
    "185.75.37.61:59166",
    "69.61.200.104:36181",
    "37.59.56.111:59166",
    "128.199.79.8:59166",
    "192.252.209.155:14455",
    "138.219.244.114:59166",
    "165.22.243.18:59166",
    "68.183.20.254:59166",
    "165.22.64.134:59166",
    "165.22.245.15:59166",
    "208.102.51.6:58208",
    "184.185.2.12:4145",
    "51.210.182.122:59166",
    "189.85.112.20:59166",
    "192.252.208.67:14287",
    "158.69.60.179:59166",
    "75.119.157.170:59166",
    "157.245.223.201:59166",
    "82.115.19.177:2237",
    "68.183.25.31:59166",
    "172.105.119.124:1080",
    "194.163.160.116:59166",
    "184.170.249.65:4145",
    "116.118.50.231:59166",
    "14.165.245.206:1080",
    "157.230.37.135:59166",
    "72.49.49.11:31034",
    "95.213.228.10:59166",
    "167.172.178.242:59166",
    "206.220.175.2:4145",
    "164.90.152.213:59166",
    "192.252.215.5:16137",
    "142.54.235.9:4145",
    "178.62.253.154:59166",
    "206.189.85.92:59166",
    "142.54.231.38:4145",
    "142.54.229.249:4145",
    "194.163.189.206:59166",
    "107.170.81.141:59166",
    "103.152.254.160:10080",
    "194.163.182.132:59166",
    "5.189.159.215:59166",
    "205.240.77.164:4145",
    "178.62.100.151:59166",
    "147.135.5.177:62213",
    "159.89.163.128:59166",
    "67.207.89.36:59166",
    "198.8.94.174:39078",
    "174.138.4.227:59166",
    "75.119.159.58:59166",
    "142.54.228.193:4145",
    "108.61.85.209:7410",
    "192.252.214.20:15864",
    "51.91.248.255:59166",
    "31.43.203.100:1080",
    "128.199.55.164:4430",
    "184.170.245.148:4145",
    "103.16.199.166:59166",
    "167.99.168.124:59166",
    "198.8.84.3:4145",
    "142.54.239.1:4145",
    "51.77.211.89:37301",
    "109.206.182.50:1080",
    "162.243.246.60:59166",
    "138.68.245.25:59166",
    "200.35.157.156:59166",
    "5.181.252.102:59166",
    "51.178.51.28:59166",
    "95.111.239.124:59166",
    "140.83.49.193:1080",
    "51.83.78.141:59166",
    "45.158.230.159:24100",
    "194.163.163.245:59166",
    "165.227.79.99:59166",
    "178.62.144.84:59166",
    "138.197.186.172:59166",
    "157.245.214.241:59166",
    "51.255.46.210:59166",
    "51.68.74.150:59166",
    "45.158.230.159:24115",
    "163.47.214.157:59166",
    "161.35.40.69:59166",
    "87.98.158.205:59166",
    "159.89.90.162:59166",
    "152.67.66.37:1080",
    "58.22.60.174:1080",
    "174.138.6.8:59166",
    "52.57.197.196:26007",
    "151.80.29.232:59166",
    "206.189.117.108:59166",
    "188.166.208.222:59166",
    "146.59.152.52:59166",
    "104.248.9.228:56237",
    "125.66.165.154:7302",
    "192.111.130.5:17002",
    "138.68.124.120:59166",
    "74.119.144.60:4145",
    "160.119.127.43:59166",
    "104.248.167.16:59166",
    "192.111.134.10:4145",
    "46.241.57.29:1080",
    "81.68.251.144:7891",
    "144.91.120.165:7497",
    "207.180.213.101:59166",
    "51.77.192.111:59166",
    "107.170.18.230:59166",
    "199.58.185.9:4145",
    "45.169.70.9:59166",
    "192.252.220.92:17328",
    "44.204.200.4:8088",
    "167.172.102.125:59166",
    "93.184.12.99:1080",
    "178.62.117.246:59166",
    "59.9.158.33:1080",
    "192.111.139.162:4145",
    "119.82.226.232:59166",
    "104.37.135.145:4145",
    "37.18.73.94:5566",
    "192.111.129.145:16894",
    "47.243.95.228:10080",
    "159.69.153.169:5566",
    "168.196.160.62:59166",
    "118.27.0.171:59166",
    "192.252.211.197:14921",
    "68.183.219.54:59166",
    "198.74.58.55:59166",
    "172.104.20.199:59166",
    "178.128.177.166:59166",
    "68.183.178.172:62861",
    "47.100.184.89:80",
    "103.43.45.20:59166",
    "167.99.214.171:59166",
    "142.44.241.192:59166",
    "103.149.53.120:59166",
    "184.170.248.5:4145",
    "138.197.13.93:59166",
    "51.68.50.41:59166",
    "167.172.119.162:59166",
    "128.199.128.10:59166",
    "192.111.137.35:4145",
    "199.58.184.97:4145",
    "138.197.11.186:59166",
    "159.65.245.126:59166",
    "188.120.248.106:59166",
    "192.111.135.17:18302",
    "200.55.247.3:59166",
    "207.154.240.108:59166",
    "192.111.137.37:18762",
    "173.255.216.8:59166",
    "51.222.146.133:59166",
    "206.189.118.100:59166",


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
        url_p = "https://ipv4.webshare.io"

        msg_ad = ""
        msg_o = f"{'O' if proxy != 'L' else 'L'} | "

        try:
            r = getImpress(url, user_agent, proxy)
            r_p = getImpress(url_p, user_agent, proxy).text
            msg_ad += f"{r_p} || "
            msg_ad += f"{url_ad[2]}"
        except:
            msg_ad += f"death - {proxy}"

        try:
            if (r.status_code == 200):
                data = r.text
                if data != '':
                    jsonD = json.loads(data)
                else:
                    jsonD = False
            else:
                jsonD = False
        except:
            jsonD = False

        resp = jsonD

        if resp != False:
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
