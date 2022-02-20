import os
from urllib.request import Request, quote, unquote, urlopen
import urllib3
import urllib
import urllib.parse
import re
import threading
import time
import requests
import sys
import io

try:
    from bs4 import BeautifulSoup
except:
    os.system('pip install BeautifulSoup4')


class DownloadThread(threading.Thread):
    def __init__(self, aurl, times):
        threading.Thread.__init__(self)
        self.aurl = aurl
        self.times = times

    def run(self):
        global save_dir
        urllib.request.urlretrieve(self.aurl, save_dir + "\\" + str(self.times) + " " + titleb + ".mp4", huidiao)


def huidiao(block_num, block_size, total_size):
    sys.stdout.write('\r>> 正在下载此番剧，总体进度： %.1f%%' % (float(block_num * block_size) / float(total_size) * 100.0))
    sys.stdout.flush()


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
title = 0
titleb = "未命名"
title_all_name = "未命名"
urls = []
lines_num = []
save_dir = input("请输入默认保存的路径：")
if save_dir == "":
    save_dir = "X:\hiden\Download"
for line in open("urls.txt"):
    line_num = re.findall(r"http://www.yinghuacd.com/show/(.*).html", line)
    l = line_num[0]
    lines_num.append(l)
if not lines_num:
    input("请在根目录下urls.txt文件输入需要下载的网址！")
    exit(0)

for vedioid in lines_num:
    for i in range(1, 101):
        htmlurl = "http://www.yhdm.io/v/" + str(vedioid) + "-" + str(i) + ".html"

        r = requests.get(htmlurl, headers=header)
        r.encoding = 'utf-8'
        html_data = r.text
        soup = BeautifulSoup(html_data, 'lxml')

        targetcontext = re.findall(r"data-vid=\"(.*mp4)\$", str(soup))
        titlea = re.findall(r"<title>(.*) ", str(soup))
        if i == 1:
            if titlea == []:
                print(soup)
                print("没有获取到标题信息！")
                if titlea[0] == '404 Not':
                    print("查询标题时返回404 Not Found.")
                print("使用id号来代替标题。")
                titleb = str(vedioid)
            else:
                titleb = titlea[0]
                print("获取到标题：" + titleb)
        if targetcontext == "":
            print("第" + str(i) + "集爬取失败")
        else:
            if targetcontext == []:
                print("该番剧视频地址全部爬取完毕！")
                break
            urls.append(targetcontext)
            print("第" + str(i) + "集爬取成功，url=" + str(targetcontext[0]) + "，标题：" + titleb)

    print("爬取完毕，开始下载")
    threads = []
    for i in urls:
        title += 1
        aurl = unquote("".join(i), encoding='utf-8')
        try:
            thread = DownloadThread(aurl, title)
            thread.start()
            threads.append(thread)
        except:
            print("\n第" + str(title) + "集下载失败", " 请求url=" + aurl)
    for t in threads:
        t.join()
    print("-----------------------------\n番剧：" + titleb + " 下载完成！\n-----------------------------")
print("所有番剧都下载完成！")
os.system("pause")
