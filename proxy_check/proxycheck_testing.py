import os, requests, re, json
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

# try out a random proxy get library
def get_proxy_online():
    proxy_online = []
    proxies = proxlist.list_proxies()
    for i in range(len(proxies)):
        ip, port = proxies[i].split(":")
        proxies[i] = (ip, int(port))
    proxy_online.extend(proxies)
    return proxy_online

# self explanatory, get your ISP's assigned IP
def get_current_ip():
    response = requests.get('https://ipinfo.io/json')
    ip_return = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(response.text))
    try:
        return ip_return[0]
    except Exception as m:
        return None

def requests_proxy_test(proxy):
    # proxies_list = get_proxy_files()
    current_ip = get_current_ip()
    # try:
    #     proxies_list.extend(get_proxy_files())
    # except Exception as m:
    #     print(m)
    url1 = 'https://ipinfo.io/json'
    ip, port = proxy
    for protocol in ['http', 'https', 'socks4', 'sock5']:
        test_proxies = {
            'http'  : f'{protocol}://{ip}:{port}',
            'https' : f'{protocol}://{ip}:{port}'
        }
        try:
            response1 = requests.get(url1, proxies=test_proxies, timeout=5)
            ip_return = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(response1.text))
            if ip_return == [] or (current_ip in ip_return): pass
            else: print(f'{protocol} {ip} {port}')
        except requests.ConnectionError as m:
            # print(m)
            pass
        except Exception as e:
            pass

def runThread(ProxyCheck, uncheckedProxies, workerCountInput):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(workerCountInput)) as executor:
            #Running ProxyCheck funtion with the unchecked proxies as its argument
            executor.map(ProxyCheck, uncheckedProxies)
        
    except Exception:
        print("Proxy Checker initiation failed! Please check you have selected a thread count.")

if __name__ == "__main__":
    proxies = get_proxy_files()
    runThread(requests_proxy_test, proxies, 200)
    

