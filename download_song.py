#coding:utf-8
import urllib
import urllib2
import traceback
import os
import json
from bs4 import BeautifulSoup

url = "http://5sing.kugou.com/XXXX/fc/%s.html"

FIRSTPAGE = 1
LASTPAGE = 13

dstpath = "h:/song"

#chrome浏览器为例，登录5sing后，f12打开开发者工具，查看点击下载按钮时传递的请求处的header里的cookie值，填入下方
cookie = ''''''
headers = {'cookie': cookie}

if not os.path.exists(dstpath):
    os.mkdir(dstpath)

def save(content,name):
    cpath = dstpath + "/" + str(name) + ".mp3"
    with open(cpath, "wb") as f:
        f.write(content)
    return cpath

def download():
    index = 0
    for i in range(FIRSTPAGE, LASTPAGE+1):
        curl = url%(i,)
        try:
            html = urllib.urlopen(curl).read()
            soup = BeautifulSoup(html, "html.parser")
            song_list = soup.find_all(class_="song_list")[0].find_all("li")
            if song_list is not None and len(song_list) > 0:
                for item in song_list:
                    name = item.find_all("a")[1].attrs["title"]
                    download_url = item.find_all("a", attrs={"title":"下载歌曲"})[0].attrs["href"]
                    songid = download_url.split("/")[-1]
                    real_download_url = "http://service.5sing.kugou.com/song/getPermission?jsoncallback=jQuery17024964711692205444_1517548341927&songId=%s&songType=2&_=1517548414034"%(songid,)
                    req = urllib2.Request(real_download_url, headers=headers)
                    download_permission_msg = urllib2.urlopen(req).read()
                    download_permission_msg = json.loads(download_permission_msg[download_permission_msg.index("(")+1:-1])

                    if "success" in download_permission_msg.keys():
                        filename = download_permission_msg["data"]["fileName"]
                        index += 1
                        req1 = urllib2.Request(filename, headers=headers)
                        content = urllib2.urlopen(req1).read()
                        cpath = save(content, index)
                        print "name:", name, "dstpath:",cpath
                    else:
                        print "name:", name, " can not download. message:", download_permission_msg["message"]
                    cdstpath = dstpath
        except Exception:
            traceback.print_exc()

    print "done!"

if __name__ == '__main__':
    download()
