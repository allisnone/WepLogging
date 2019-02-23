# -*- coding: utf-8 -*-
#if ssl, you need to add ASWG CA to following file
#__Author__= allisnone 2018-08-01
#/root/.pyenv/versions/3.5.5/lib/python3.5/site-packages/certifi/cacert.pem
import argparse
import re
import os
import csv
import string,sys
import requests
from urllib.parse import quote
from multiprocessing import Pool


def set_proxy(url, proxy=''):
    """
    根据URL设置使用HTTP或者HTTPS的代理
    :param url: str type , dest url
    :param proxy: str type, <proxy_IP>:<proxy_port>, like  172.18.230.23:8080
    """
    if not proxy:
        return {}
    aswg_proxy = 'http://' + proxy
    if "https://" in url:
        return {'https': aswg_proxy}
    return {'http': aswg_proxy} 
 
def get_urls_from_web(base_url,proxy={}):
    """
    用于病毒测试，模拟下载病毒文件 
    如'http://172.16.0.1/upload/VirusSamples/'
    :param base_url: str，  通常是用于存放病毒文件的某个url目录
    :param proxy: dict， proxy的字典类型
    :return: list， URL_list（Generator）
    """
    result = ''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        print('before request')
        r = requests.get(base_url, headers=headers, proxies=proxy, verify=False)
        print(r.status_code)
        result = r.text
    except Exception as e:
        print(e)
    if result:
        # pattern = re.compile(r"alt=\"\[(?!DIR|ICO).*?<a href=.*?>(.*?)</a>", re.S)
        pattern = re.compile(r"<a href=.*?>(.*?)</a>", re.S)
        fn = re.findall(pattern, result)
        return [base_url + i for i in fn]

def get_urls_from_file(from_file='url16000.txt'):
    """
    用于url分类测试，测试文件中存放大量的url地址
    :param from_file: str 
    :return: list， URL_list（Generator）
    """
    txtfile = open(from_file, 'r')#'encoding='utf-8')
    url_list = txtfile.readlines()
    for i in range(0,len(url_list)):
        url_list[i] = url_list[i].replace('\n','')
        protocol_header = url_list[i][:9].lower()
        if "http://" in protocol_header or "https://" in protocol_header:
            pass
        else: #无协议头部，默认加http协议
            url_list[i] = "http://" + url_list[i]
    return url_list
    
    
def encode_url(url):
    """
    处理包含中文字符串/空格的URL编码问题
    :param url:
    :return:
    """
    return quote(url, safe=string.printable).replace(' ', '%20')


def write2csv(data,file='result.csv'):
    try:
        with open(file, 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
    except Exception as e:
        print(e)

def http_request(url,proxy='',block_info='访问的URL中含有安全风险',encoding='utf-8'):
    """
    下载文件，分析是否被SWG阻断
    :param url:
    :return: callback
    """
    block_info = '访问的URL中含有安全风险'
    try:
        #r = requests.get(encode_url(url), proxies=PROXIES, verify=False)
        r = requests.get(encode_url(url), proxies=set_proxy(url, proxy))
        print(url, r.status_code)
        if r.status_code == 403:
            r.encoding = encoding
            if block_info in r.text:
                return [url, url.split('/')[-1], r.status_code, block_info]
            else:
                return [url, url.split('/')[-1], r.status_code, "other"]
        else:
            return [url, url.split('/')[-1], r.status_code, 'pass']
    except Exception as e:
        print(e)
        return [url, url.split('/')[-1], 0, e]

def request_results(url,proxy='',file='result.csv',type='url'):
    result = http_request(url, proxy)
    write2csv(result, file)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='该Python3脚本用于ASWG做URL分类测试和病毒测试。\n 1、URL测试使用方法:\n python aswgRequest.py -t url -f ulrs.txt -p 172.18.230.23:8080 -o urls_result.csv \n 2、病毒测试：  python aswgRequest.py -t virus -u http://www.sogaoqing.com/upload/VirusSamples/ -p 172.18.230.23:8080 -o virus_result.csv') 
    parser.add_argument('-t','--type', type=str, default='url',help='默认为url分类测试，从文件读取url地址；当设置为virus时，将模拟从某个web服务器特定目录下载所有文件。')
    parser.add_argument('-p','--proxy', type=str, default = '',help='默认不适用aswp代理，需指定代理时，<proxy_IP>:<proxy_port> 例如：72.18.230.23:8080') 
    parser.add_argument('-f','--url-file', type=str, default= 'urls.txt',help='默认为urls.txt， 指定包含需要测试url的文件，每行一条url。')
    parser.add_argument('-u','--url-base', type=str, default= '',help='默认为空，用于模拟下载病毒测试，指定url目录，如： http://172.16.0.1/upload/VirusSamples/')
    parser.add_argument('-o','--out-put', type=str, default='result.csv',help='默认为result.csv，测试结果保存为csv文件。')
    args = parser.parse_args()
    type = args.type
    proxy = args.proxy
    url_file = args.url_file
    result_file = args.out_put
    url_base = args.url_base
    #date_str = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
    if os.path.exists(result_file):
        os.remove(result_file)
    urls = []
    if type=='url':
        urls = get_urls_from_file(from_file=url_file)
    elif type=='virus':
        if url_base:
            urls = get_urls_from_web(url_base)
        else:
            print('ERROR: 缺少指定URL下载目录，退出')
            sys.exit()
    else:
        print('ERROR: 测试类型错误，退出')
        sys.exit()
    print('---------------------开始 %s 测试-------------------------------------------' % type )
    if urls:
        print('待测试URL总数为： ', len(urls))
    else:
        print('ERROR: 获取url失败，退出')
        sys.exit()
    print('ASWG Proxy 为: ', proxy)
    pool = Pool()
    for url in urls:
        #pool.apply_async(http_request, (url, proxy), callback=write2csv)
        pool.apply_async(request_results, (url, proxy,result_file))
    pool.close()
    pool.join()
    print('测试结果位于： ', result_file )
    print('---------------------测试 %s 完成-------------------------------------------' % type )
    """URL测试使用方法"""
    #python aswgRequest.py -t url -f urls.txt -p 172.18.230.23:8080 -o urls_result.csv
    #python aswgRequest.py -t url -f urls.txt -p 172.18.200.240:8080 -o urls_result.csv
    """病毒测试使用方法，模拟http下载病毒"""
    #python aswgRequest.py -t virus -u http://www.sogaoqing.com/upload/VirusSamples/ -p 172.18.230.23:8080 -o virus_result.csv
    

