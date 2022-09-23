import os, requests, json
from glob import glob
import concurrent.futures


def get_proxy_files():
    proxy_from_file = []
    #path = os.getcwd() + f'/{folder}/'
    path = os.getcwd() + '/proxy_check/proxy_file/'

    #read all proxy files in folder, turn it into a list of tuples of (ip, port)
    for filename in glob(os.path.join(path, '*txt')):
        proxy_read = open(filename, 'r', encoding='utf-8').read().split()
        for i in range(len(proxy_read)):
            ip, port = proxy_read[i].split(":")
            proxy_read[i] = (ip, int(port))
        proxy_from_file.extend(proxy_read)
    return proxy_from_file

def get_proxies_online():
    proxies = []
    proxy_remote = {
        "urls" :[
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all&timeout=500&country=all&ssl=all",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all",
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://www.proxyscan.io/download?type=socks5",
        "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all&ssl=all&anonymity=all"
        ]
    }
    '''
    the funny thing about this list of socks5 proxy urls is none of them are actually socks5
    they contain a mixture of http and socks4, but never socks5
    i genuinely don't know why, home router with OpenWRT misconfiguration?
    '''
    for proxy_site in proxy_remote['urls']:
        try:
            response = requests.get(proxy_site)
            proxy_get = (response.text).split()
            for i in range(len(proxy_get)):
                ip, port = proxy_get[i].split(":")
                proxy_get[i] = (ip, int(port))
            proxies.extend(proxy_get)

        except requests.ConnectionError() as m:
            print(f'Error while getting proxies from {proxy_site}: {m}')
    return proxies
        
# self explanatory, get your ISP's assigned IP
def get_current_ip():
    response = requests.get('https://ipinfo.io/json')
    try:
        ip_return = json.loads(response.text)['ip']
        return ip_return
    except Exception as m:
        return None

def requests_proxy_test(proxy):
    
    url = 'https://ipinfo.io/json'
    ip, port = proxy
    for protocol in ['http', 'https', 'socks4', 'socks5']:
        test_proxies = {
            'http'  : f'{protocol}://{ip}:{port}',
            'https' : f'{protocol}://{ip}:{port}'
        }
        try:
            response = requests.get(url, proxies=test_proxies, timeout=0.8)
            ip_return = json.loads(response.text)['ip']
            if (ip_return == None) or (current_ip == ip_return): pass
            else: print(f'{protocol} {ip} {port}')
        except requests.ConnectionError as m:
            # print(m)
            pass
        except Exception as e:
            # print(e)
            pass

def runThread(ProxyCheck, uncheckedProxies, workerCountInput):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(workerCountInput)) as executor:
            #Running ProxyCheck funtion with the unchecked proxies as its argument
            executor.map(ProxyCheck, uncheckedProxies)
        
    except Exception:
        print("Proxy Checker initiation failed! Please check you have selected a thread count.")

if __name__ == "__main__":
    current_ip = get_current_ip()
    proxies = get_proxies_online()
    runThread(requests_proxy_test, proxies, 200)
    

