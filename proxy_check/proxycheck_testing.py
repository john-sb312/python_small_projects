import os, requests, json
from glob import glob
import concurrent.futures

PATH = os.getcwd() + '/proxy_check/'

def get_proxy_files():
    proxy_from_file = []
    path = PATH + '/proxy_file/'

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
    } # i prefer socks5, but you can add any 
    for proxy_site in proxy_remote['urls']:
        try:
            response = requests.get(proxy_site, timeout=1)
            proxy_get = (response.text).split()
            for i in range(len(proxy_get)):
                ip, port = proxy_get[i].split(":")
                proxy_get[i] = (ip, int(port))
            proxies.extend(proxy_get)

        except Exception as m:
            print(f'Error while getting proxies from {proxy_site}: {m}')
        except Exception as e:
            print(e)
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
    protos_proxy = []
    url = 'https://ipinfo.io/json'
    ip, port = proxy
    for protocol in ['http', 'https', 'socks4', 'socks5']:
        test_proxies = {
            'http'  : f'{protocol}://{ip}:{port}',
            'https' : f'{protocol}://{ip}:{port}'
        }
        try:
            response = requests.get(url, proxies=test_proxies, timeout=0.8)
            result_return = json.loads(response.text)
            if (result_return['ip'] == None) or (current_ip == result_return['ip']): pass
            else: protos_proxy.append(protocol)
        except requests.ConnectionError as m:
            pass
        except Exception as e:
            pass
    if protos_proxy == []: pass 
    else: 
        online_proxy = {
            f'{ip}:{port}': {
                'protocol'  : protos_proxy,
                'city'      : result_return['city'],
                'region'    : result_return['region'],
                'country'   : result_return['country'],
                'location'  : result_return['loc']
                }
            }
        try :
            alive.update(online_proxy)
        except Exception() as e: print(e)
        print(online_proxy)
        


def run_thread(worker, input, worker_count):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(worker_count)) as executor:
            executor.map(worker, input)
    except Exception as e:
        print(f'Error, {e}.')

if __name__ == "__main__":
    alive = {}
    current_ip = get_current_ip()
    proxies = get_proxies_online()
    run_thread(requests_proxy_test, proxies, 100)
    
    dumping = json.dumps(alive, indent=4)
    with open(PATH + "online_proxies.json", "w") as outfile:
        outfile.write(dumping)