import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json
from concurrent.futures import ThreadPoolExecutor

base_url = 'https://pandas.pydata.org/docs/reference/index.html'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
    'cookie': '_ga=GA1.2.877562792.1646187557; _gid=GA1.2.1652739076.1646187561; __utma=172570402.877562792.1646187557.1646187557.1646192143.2; __utmc=172570402; __utmz=172570402.1646192143.2.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
}

def find_fun_urls(base_url):
    """查找pandas所有可用函数的api reference的链接"""
    fun_urls = []
    res = requests.get(base_url, headers=header)
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup.select('#bd-docs-nav > div > ul > li a')
    for tag in tags:
        tag_url = urljoin(base_url, tag.attrs['href'])
        res = requests.get(tag_url, headers=header)
        res.encoding = 'utf-8'
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        funs = soup.select('ul li.toctree-l2  a.reference.internal')
        for fun in funs:
            fun_url = urljoin(base_url, fun.attrs['href'])
            fun_urls.append(fun_url)
    return fun_urls

def fun_doc_spider(fun_url, out_path):
    """爬取函数文档，删除文档中不必要的元素，保存文档同时返回各个文档的路径等信息以便添加到程序员手册中"""
    fun_name = os.path.basename(fun_url)[:-5] # 函数名
    res = requests.get(fun_url, headers=header)
    res.encoding = 'utf-8'
    html = res.text
    # 删除页面中多余的元素
    soup = BeautifulSoup(html, 'html.parser')
    selectors = ['#navbar-main',
                'body > div.container-xl > div > div.col-12.col-md-3.bd-sidebar',
                'body > div.container-xl > div > div.d-none.d-xl-block.col-xl-2.bd-toc',
                'body > footer', 
                'body > div.container-xl > div > main > div.prev-next-area',
                '#{} > dl > dd > div.admonition.seealso'.format(fun_name.replace('.', '-').replace('_', '-'))]
    for selector in selectors:
        try:
            element = soup.select(selector)[0]
            element.extract()
        except:
            continue
    
    # 保存文档
    out_html_path = os.path.join(out_path, os.path.basename(fun_url))
    with open(out_html_path, 'w', encoding='utf-8') as fp:
        fp.write(str(soup))

    # 文档设置
    try:
        # 获取文档描述信息
        fun_desc_selector = "#{} > dl > dd > p:nth-child(1)".format(fun_name.replace('.', '-').replace('_', '-'))
        fun_desc = soup.select(fun_desc_selector)[0].text
    except:
        fun_desc = fun_name
    fun_setting = {
                    "name": fun_name,
                    "type": "pandas",
                    "path": out_html_path,
                    "desc": fun_desc
                }
    return fun_setting

if __name__ == '__main__':
    out_path = './api'
    fun_urls = find_fun_urls(base_url)
    print("共计{}个函数，开始下载各个函数的文档".format(len(fun_urls)))

    # 多线程下载各个函数的文档
    with ThreadPoolExecutor(max_workers=20) as pool:
        fun_settings = pool.map(fun_doc_spider, fun_urls, [out_path]*len(fun_urls))

    with open('./pandas.json', 'w', encoding='utf-8') as fp:
        json.dump(list(fun_settings), fp)

    print("下载完成")