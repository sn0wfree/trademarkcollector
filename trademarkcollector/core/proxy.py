# coding=utf8
import requests

proxy_host_url = "http://112.74.189.154:5010/"


def get_proxy(proxy_host_url="http://112.74.189.154:5010/"):
    proxy_port = requests.get(proxy_host_url + "get/").content.decode()
    proxy, port = proxy_port.split(':')
    return proxy, port


def monitor_proxy(proxy_host_url="http://112.74.189.154:5010/"):
    return requests.get(proxy_host_url + "get_status/").content.decode()


def delete_proxy(proxy, proxy_host_url="http://112.74.189.154:5010/"):
    return requests.get("{}/delete/?proxy={}".format(proxy_host_url, proxy))


def get_proxy_and_delete(proxy_host_url="http://112.74.189.154:5010/", verbose=False):
    proxy_port = requests.get(proxy_host_url + "get/").content.decode()
    r = delete_proxy(proxy_port)
    if verbose:
        print(r.text)
    proxy, port = proxy_port.split(':')
    return proxy, port


if __name__ == '__main__':
    pass
