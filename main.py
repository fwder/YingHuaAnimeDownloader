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
    sys.stdout.write('\r>> �������ش˷��磬������ȣ� %.1f%%' % (float(block_num * block_size) / float(total_size) * 100.0))
    sys.stdout.flush()


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
title = 0
titleb = "δ����"
title_all_name = "δ����"
urls = []
lines_num = []
save_dir = input("������Ĭ�ϱ����·����")
if save_dir == "":
    save_dir = "X:\hiden\Download"
for line in open("urls.txt"):
    line_num = re.findall(r"http://www.yinghuacd.com/show/(.*).html", line)
    l = line_num[0]
    lines_num.append(l)
if not lines_num:
    input("���ڸ�Ŀ¼��urls.txt�ļ�������Ҫ���ص���ַ��")
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
                print("û�л�ȡ��������Ϣ��")
                if titlea[0] == '404 Not':
                    print("��ѯ����ʱ����404 Not Found.")
                print("ʹ��id����������⡣")
                titleb = str(vedioid)
            else:
                titleb = titlea[0]
                print("��ȡ�����⣺" + titleb)
        if targetcontext == "":
            print("��" + str(i) + "����ȡʧ��")
        else:
            if targetcontext == []:
                print("�÷�����Ƶ��ַȫ����ȡ��ϣ�")
                break
            urls.append(targetcontext)
            print("��" + str(i) + "����ȡ�ɹ���url=" + str(targetcontext[0]) + "�����⣺" + titleb)

    print("��ȡ��ϣ���ʼ����")
    threads = []
    for i in urls:
        title += 1
        aurl = unquote("".join(i), encoding='utf-8')
        try:
            thread = DownloadThread(aurl, title)
            thread.start()
            threads.append(thread)
        except:
            print("\n��" + str(title) + "������ʧ��", " ����url=" + aurl)
    for t in threads:
        t.join()
    print("-----------------------------\n���磺" + titleb + " ������ɣ�\n-----------------------------")
print("���з��綼������ɣ�")
os.system("pause")
