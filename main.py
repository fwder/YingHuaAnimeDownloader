# coding=utf-8
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
        global error_flag
        # 设置单线程标志位
        for i in range(1,11):
            try:
                urllib.request.urlretrieve(self.aurl,
                                           save_dir + "\\" + titleb + "\\" + str(self.times) + " " + titleb + ".mp4",
                                           huidiao)
                flap = True
            except:
                print("\n第 "+str(self.times)+" 集下载发生错误，30s后准备重试...")
                flap = False
                time.sleep(30)
                continue
            if flap: # 无报错下载完毕
                # 设置全局标志位
                error_flag = True
                print("\n第 "+str(self.times)+" 集下载完毕。")
                break
        # 报错超过10次
        print("\n第 "+str(self.times)+" 集下载发生错误并且超过5次，建议检查VPN连接是否可用或者IP是否被封！退出线程...")


def isMakeDir(path):
    # 创建文件夹
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)


def huidiao(block_num, block_size, total_size):
    sys.stdout.write('\r>> 正在下载此番剧，总体进度： %.1f%%' % (float(block_num * block_size) / float(total_size) * 100.0))
    sys.stdout.flush()


def newURLtoUsedAndOld():
    lines = open('urls_new.txt').readlines()
    open('urls_used.txt','a').write(lines[0])
    open('urls_old.txt','a').write(lines[0])
    open('urls_new.txt', 'w').writelines(lines[1:])

def newURLtoUsedAndBad():
    lines = open('urls_new.txt').readlines()
    open('urls_used.txt','a').write(lines[0])
    open('urls_bad.txt','a').write(lines[0])
    open('urls_new.txt', 'w').writelines(lines[1:])

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
for line in open("urls_new.txt"):
    line_num = re.findall(r"http://www.yinghuacd.com/show/(.*).html", line)
    l = line_num[0]
    lines_num.append(l)
if not lines_num:
    input("请在根目录下urls_new.txt文件输入需要下载的网址！")
    exit(0)

for vedioid in lines_num:
    for i in range(1, 99999):
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
                print("使用id号来代替标题。")
                titleb = str(vedioid)
            elif titlea[0] == '404 Not':
                print("查询标题时返回404 Not Found.")
                print("使用id号来代替标题。")
                titleb = str(vedioid)
            else:
                titleb = titlea[0]
                print(
                    "\n-----------------------------\n番剧：" + titleb + " 开始下载！\n读取到番剧地址：http://www.yinghuacd.com/show/" + str(
                        vedioid) + ".html\n-----------------------------\n")
        if targetcontext == "":
            print("第" + str(i) + "集爬取失败")
        else:
            if targetcontext == []:
                print("该番剧视频地址全部爬取完毕！")
                break
            urls.append(targetcontext)
            print("第" + str(i) + "集爬取成功，url=" + str(targetcontext[0]) + "，标题：" + titleb)

    print("爬取完毕，开始下载（直链下载不消耗VPN流量）")
    threads = []
    isMakeDir(save_dir + "\\" + titleb)
    # 标志位，检查是否所有线程全部出错
    error_flag = False
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
    title = 0
    urls = []
    # 检查标志位是否为True，若为False则是全部出错
    if error_flag:
        newURLtoUsedAndOld()
        print("\n-----------------------------\n番剧：" + titleb + " 下载完成！\n-----------------------------\n")
    else:
        newURLtoUsedAndBad()
        print("\n-----------------------------\n番剧：" + titleb + " 下载失败！请到urls_bad.txt查看失败的地址并尝试重新下载！\n-----------------------------\n")

print("所有番剧都下载完成！")
os.system("pause")
