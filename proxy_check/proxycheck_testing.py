import os, requests, re
from glob import glob


def get_proxy_files():
    proxy_from_file = []
    #path = os.getcwd() + f'/{folder}/'
    path = os.getcwd() + '/proxy_file/'

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

def requests_proxy_test():
    proxies_list = []
    current_ip = get_current_ip()
    try:
        proxies_list.extend(get_proxy_files())
    except Exception as m:
        print(m)
    url1 = 'https://ipinfo.io/json'
    for proxy in proxies_list:
        ip, port = proxy
        test_proxies = {
            'http'  : f'socks5://{ip}:{port}',
            'https' : f'socks5://{ip}:{port}'
        }
        try:
            response1 = requests.get(url1, proxies=test_proxies, timeout=(0.5, 0.5))
            ip_return = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(response1.text))
            if ip_return == [] or (current_ip in ip_return): pass
            else: print(f'socks5 {ip} {port}')

        except requests.ConnectionError as m:
            # print(m)
            pass
        except Exception as e:
            pass
if __name__ == "__main__":
    requests_proxy_test()
    # print(get_current_ip())