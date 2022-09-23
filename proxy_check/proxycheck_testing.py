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
    for protocol in ['http', 'https', 'socks4', 'sock5']:
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
    current_ip = get_current_ip()
    proxies = get_proxy_files()
    runThread(requests_proxy_test, proxies, 200)
    

