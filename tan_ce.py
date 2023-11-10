import requests
import logging
from hurry.filesize import size as filesize
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from fake_headers import Headers
from copy import deepcopy
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

# 判断ct是否存在敏感字符
def vlun(urltarget, proxies, header, timeout, outputfile):
    try:
        allowed_content_types = ['html', 'image', 'xml', 'text', 'json', 'javascript', 'gov']  # content_type的包含字符

        headers = header.generate()

        if proxies:
            response = requests.get(url=urltarget, headers=headers, timeout=timeout, allow_redirects=False, stream=True,
                                    verify=False, proxies=proxies)
        else:
            response = requests.get(url=urltarget, headers=headers, timeout=timeout, allow_redirects=False, stream=True,
                                    verify=False)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type').lower()  # 将ct的值转换为小写，方便比对上述的act
            if not any(allowed in content_type for allowed in allowed_content_types):  # 判断上述ct是否包含上述act，如若不包含，则执行下列代码
                tmp_rarsize = int(response.headers.get('Content-Length'))
                rarsize = filesize(tmp_rarsize)  # 使用正确的函数名
                if tmp_rarsize > 0:
                    logging.warning('[失败] {}'.format(urltarget))
                    with open(outputfile, 'a') as f:
                        f.write(str(urltarget) + '  size:' + str(rarsize) + '\n')
                else:
                    logging.warning('[失败] {}'.format(urltarget))
            else:
                logging.warning('[失败] {}'.format(urltarget))
        else:
            logging.warning('[失败] {}'.format(urltarget))
    except requests.exceptions.RequestException as e:
        logging.error(f'处理 {urltarget} 时发生错误: {str(e)}')

# 保证url的正确，确保是以http或https开头，同时以'/'结尾，确保字典输入的是根目录
def urlcheck(target, ulist):
    target = target.strip()
    parsed_url = urlparse(target)
    if not parsed_url.scheme:
        target = 'http://' + target
    if not target.endswith('/'):
        target += '/'
    ulist.append(target)
    return ulist

def dispatcher(url_file=None, url=None, max_thread=20, dic=None, outputfile=None, timeout=None):

    urllist = []

    if url_file:
        with open(url_file) as f:
            for line in f:
                urllist = urlcheck(line, urllist)
    elif url:
        urllist = urlcheck(url, urllist)

    for u in urllist:
        check_urllist = []

        ucp = u[len(u):]  # 剥去 'http://' 或 'https://'
        if '/' in ucp:
            ucp = ucp.split('/')[0]

        current_info_dic = deepcopy(dic)
        suffixFormat = ['.zip', '.rar', '.tar.gz', '.tgz', '.tar.bz2', '.tar', '.jar', '.war', '.7z', '.bak', '.sql',
                        '.gz', '.sql.gz', '.tar.tgz', '.backup']
        domainDic = [ucp, ucp.replace('.', ''), ucp.replace('.', '_')]

        for s in suffixFormat:
            for d in domainDic:
                current_info_dic.extend([d + s])

        for info in current_info_dic:
            url = u + info
            check_urllist.append(url)
            print("[添加检查] " + url)

        l = []
        p = ThreadPoolExecutor(max_thread)
        for url in check_urllist:
            obj = p.submit(vlun, url, proxies, header, timeout, outputfile)
            l.append(obj)
        p.shutdown()

if __name__ == '__main__':
    usageexample = '\n       示例: python3 ihoneyBakFileScan_Modify.py -t 100 -f url.txt -o result.txt\n'
    usageexample += '                '
    usageexample += 'python3 ihoneyBakFileScan_Modify.py -u https://www.example.com/ -o result.txt'

    parser = ArgumentParser(add_help=True, usage=usageexample, description='一个网站备份文件泄漏扫描工具。')
    parser.add_argument('-f', '--url-file', dest="url_file", help="示例: url.txt")
    parser.add_argument('-t', '--thread', dest="max_threads", nargs='?', type=int, default=1, help="最大线程数")
    parser.add_argument('-u', '--url', dest='url', nargs='?', type=str, help="示例: http://www.example.com/")
    parser.add_argument('-d', '--dict-file', dest='dict_file', nargs='?', help="示例: dict.txt")
    parser.add_argument('-o', '--output-file', dest="output_file", help="示例: result.txt")
    parser.add_argument('-p', '--proxy', dest="proxy", help="示例: socks5://127.0.0.1:1080")

    args = parser.parse_args()

    tmp_suffixFormat = ['.zip', '.rar', '.tar.gz', '.tgz', '.tar.bz2', '.tar', '.jar', '.war', '.7z', '.bak', '.sql',
                        '.gz', '.sql.gz',]

    outputfile = args.output_file  # 获取输出文件名
    max_threads = args.max_threads

    # 设置代理和请求头
    proxies = None
    header = Headers()

    # 定义字典
    dic = []

    # 调用dispatcher函数
    dispatcher(args.url_file, args.url, max_threads, dic, outputfile)


    
