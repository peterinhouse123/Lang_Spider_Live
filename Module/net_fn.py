# -*- coding: UTF-8 -*-
import requests
from pyquery import PyQuery as pq
from  Module import text_fn
import pickle
import os
import smtplib
import threading
import time

from email.mime.text import MIMEText
from email.header import Header
import urllib.parse





def download_filed(url,header_string,cookie_path,filename,proxyc="",allow_redirects=1):
    if header_string == "":
        host_preg = r"[http]+[https]+://([\w\W]+?)/"
        host = text_fn.preg_get_word(host_preg, 1, url)
        Ref = "https://www.google.com/"
        header_string = "Host: "+host+"###Connection: keep-alive###Cache-Control: max-age=0###Upgrade-Insecure-Requests: 1###User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36###Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8###Referer: "+Ref+"###Accept-Encoding: gzip, deflate, sdch###Accept-Language: zh-TW,zh;q=0.8,en;q=0.6,en-US;q=0.4,zh-CN;q=0.2"
    #print (header_string)
    #print (db.get_time()+":start_download:"+url)
    normal_header_string = header_string
    normal_header = get_header_dict(normal_header_string)
    if cookie_path != "":
        cookieg = load_cookies(cookie_path)
    else:
        cookieg = None
    # NOTE the stream=True parameter
    if proxyc == "":
        r = requests.get(url, stream=True, headers=normal_header, cookies=cookieg,allow_redirects=allow_redirects,verify=0)
    else:
        proxies = {
            'http': 'http://' + proxyc,
            'https': 'http://' + proxyc,
        }
        r = requests.get(url, stream=True, headers=normal_header, cookies=cookieg,proxies=proxies,allow_redirects=allow_redirects,verify=0)
    #print(r.status_code)


    start_download = 0
    if os.path.isfile(filename) == True:
        print(r.headers['content-length'])
        print(os.path.getsize(filename))
        if int(r.headers['content-length']) > os.path.getsize(filename):
            start_download = 1
    else:
        start_download = 1

    if start_download == 1:

        print("start_download:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        with open(filename, 'wb') as f:

            if not r.ok:
                print("error when download")
                print(r.history)
                print(r.headers)
                print(r.status_code)


            for block in r.iter_content(1024):
                f.write(block)
        print("download_success:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    return filename

def cookie_str_to_file(string,filename):
    jar = cookie_str_to_jar(string)
    save_cookies(jar,filename)


#保存cookie request.
# cookies,path
def save_cookies(requests_cookiejar, filename):
    path = text_fn.preg_get_word(r'([\w\W\\/]+\\)[\w\W]+\.', 1, filename)
    if os.path.exists(path) != True:
        os.makedirs(path)
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)
#讀取cookie
#path

def load_cookies(filename):

    if os.path.isfile(filename) and os.path.getsize(filename) > 0:

        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        open(filename,'a')
        return ""


#将字串cookie转成jar檔
def cookie_str_to_jar(cookie_str):
    cookie_dict =  cookie_str_to_dict(cookie_str)
    cj2 =  requests.utils.cookiejar_from_dict(cookie_dict)
    return cj2



#将字串cookie转成dict
def cookie_str_to_dict(cookie_str):
        cookie_c = cookie_str.split(';')
        new_cookie = dict()
        for g in cookie_c:
            g = g.strip()
            gj = g.split("=")
            if len(gj) != 2:
                continue
            new_cookie[gj[0]] = gj[1]

        # print(cookie_c)
        # print(new_cookie)
        return new_cookie
#將文字字串，轉成dict
def cookie_dict_to_str(cookie_dict):
    # end = "Cookie: "
    end = ""
    for key in cookie_dict:
        val = cookie_dict[key]
        temp = key+"="+ format(val)
        end = end + format(temp) + "; "
    return end

def post_string_to_dict(str):
    #str = "_xsrf=5c5085a0e522b1309649f566b9321e5d&password=i993oio3&captcha_type=cn&remember_me=true&email=1c9y9z3%40163.com"
    str = urllib.parse.unquote(str)

    arr = str.split("&")


    end = dict()

    for item in arr:
        temp = item.split('=',1)

        try:
            key = temp[0]
            end[key] = temp[1]
        except:
            pass

    return end
#將文字header變成陣列
def get_header_dict(string):
  # string = "Host: www.zhihu.com###Connection: keep-alive###Content-Length: 113###Accept: */*###Origin: https://www.zhihu.com###X-Requested-With: XMLHttpRequest###User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36###Content-Type: application/x-www-form-urlencoded; charset=UTF-8###Referer: https://www.zhihu.com/###Accept-Encoding: gzip, deflate, br###Accept-Language: zh-TW,zh;q=0.8,en;q=0.6,en-US;q=0.4,zh-CN;q=0.2"
    string = string.replace("https://","https#")
    string = string.replace("http://","http#")
   # print string
    arr = string.split("###")
   # print arr
    end = dict()
    for item in arr:
        if item != "":
            temp = item.split(":")
            temp[1] = temp[1].replace("https#","https://")
            temp[1] = temp[1].replace("http#","http://")
            end[temp[0].strip()] = temp[1].strip()
    return end



# 取得目前的連線ip
def get_myip(proxy="", timeout=10, test_link='http://kosmos-studio.com/proxyc/engine.php?list=check'):
    ip_test_url = test_link


    if proxy != "":

        proxies = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy,
        }
        try:
            r = requests.get(ip_test_url, proxies=proxies, timeout=timeout)
            rs = r.text
        except:
            rs = "empty_data"
            # print(rs)
    else:
        r = requests.get(ip_test_url, timeout=timeout)
        rs = r.text
    end = dict()
    if rs != "empty_data" and r.status_code == 200:
        rs_query_data = pq(rs)
        #print r.status_code

        myip = rs_query_data("b").eq(0).text()
        myip = myip.replace("Your IP: ", "")

        #print(myip)
        # patte = re.compile(r"REMOTE_ADDR: (\d+\.\d+\.+\d+\.\d+)")
        # grk = patte.search(rs)
        # print(grk.group(1))
        remote_preg = r"REMOTE_ADDR: (\d+\.\d+\.+\d+\.\d+)"
        real_ip_preg = r"HTTP_X_REAL_IP: (\d+\.\d+\.+\d+\.\d+)"
        http_client_preg = r"HTTP_CLIENT_IP: (\d+\.\d+\.+\d+\.\d+)"
        http_via_preg = r"HTTP_VIA: ([\w\W\s]*)\nREMOTE_ADDR"
        remote_ip = text_fn.preg_get_word(remote_preg, 1, rs)
        real_ip =  text_fn.preg_get_word(real_ip_preg, 1, rs)
        http_client = text_fn.preg_get_word(http_client_preg, 1, rs)
        http_via = text_fn.preg_get_word(http_via_preg, 1, rs)


        end['remote_ip'] = remote_ip
        end['real_ip'] = real_ip
        end['http_client'] = http_client
        end['http_via'] = http_via
        # end['z_real_data'] = rs
        lv = 0
        # 判斷代理等級
        if real_ip != remote_ip:
            lv = 0
        if real_ip == remote_ip:
            lv = 1
            if http_via == "empty_data":
                lv = 2
            else:
                lv = 1
        if http_client != "empty_data":
            lv = 0

        end['lv'] = lv
        end['stat'] = 1
        #判斷ip國家
        geo_data = get_ip_geolocation(real_ip)
        end['geo'] = geo_data['geo']

    else:
        end['stat'] = 0


    return end


def get_ip_geolocation(real_ip):

    geo_key = "4eca66b6f53c100258e122d069e244a6ab5b88df3eab68d59ef8ebdd0727c751"
    geo_url = "http://api.ipinfodb.com/v3/ip-city/?key=" +  geo_key + "&ip=" + real_ip

    rs = requests.get(geo_url)
    con = rs.content
    arr = str(con).split(";")
    end = dict()
    end['geo'] = arr[3]
    end['geo_all_name'] = arr[4]
    end['city'] = arr[5]


    return end
def header_set_cookie(set_cookie_data,cookie_path):

    set_cookie_data = set_cookie_data.split(",")

    for bb in set_cookie_data:
            temp_bb = bb.split(';')
            if '=' in temp_bb[0]:

                cdata = temp_bb[0].split('=')
                print(cdata)
                edit_cookie(cookie_path,cdata[0],cdata[1])


def read(url, header_string="",cookie_path ="",proxy = "",timeout = 20,allow_redirects = True,show_cookie_setting = False ):

    if header_string == "":
        host_preg = r"[http]+[https]+://([\w\W]+?)/"
        host = text_fn.preg_get_word(host_preg, 1, url)
        Ref = "https://www.google.com/"
        header_string = "Host: "+host+"###Connection: keep-alive###Cache-Control: max-age=0###Upgrade-Insecure-Requests: 1###User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36###Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8###Referer: "+Ref+"###Accept-Encoding: gzip, deflate, sdch###Accept-Language: zh-TW,zh;q=0.8,en;q=0.6,en-US;q=0.4,zh-CN;q=0.2"
    #print (header_string)
    # print (db.get_time()+":start_read:"+url)
    normal_header_string = header_string
    normal_header = get_header_dict(normal_header_string)
    #print url
    verify_sta = 0


    if proxy != "":
        proxy = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy,
        }
        verify_sta = False

    if cookie_path == "":
        # print(normal_header)
        page = requests.get(url, headers=normal_header,proxies=proxy,verify=verify_sta,timeout = timeout,allow_redirects = allow_redirects)

    else:
        cookieg = load_cookies(cookie_path)
     #   print(len(cookieg))
       # print cookieg
        page = requests.get(url, headers=normal_header, cookies=cookieg,proxies=proxy,verify=verify_sta,timeout = timeout,allow_redirects = allow_redirects)
        #page.cookies.update(cookieg)
        handler = {}


        for bb in page.cookies:
            if show_cookie_setting == True:
                print(bb.name+":"+str(bb.value))

            edit_cookie(cookie_path,bb.name,bb.value)

        if 'Set-Cookie'in page.headers:

            header_set_cookie(page.headers['Set-Cookie'],cookie_path)

    return page

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def json_poster(url,data, header_string,cookie_path ="",proxy = "",timeout = 20,show_cookie_setting = False):
    normal_header_string = header_string
    normal_header = get_header_dict(normal_header_string)
    # print(normal_header)
    verify_sta = False
    if proxy != "":
        proxy = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy,
        }
        verify_sta = False


    if cookie_path == "":

        page = requests.post(url,data,headers=normal_header,proxies=proxy,verify=verify_sta,timeout = timeout)
        # print(page)
        # print(url)
    else:
        cookieg = load_cookies(cookie_path)

        page = requests.post(url,data, headers=normal_header, cookies=cookieg,proxies=proxy,verify=verify_sta,timeout = timeout)


        #page.cookies.update(cookieg)

        for bb in page.cookies:

            if show_cookie_setting == True:
                print(bb.name+":"+str(bb.value))

            edit_cookie(cookie_path,bb.name,bb.value)
        #save_cookies(page.cookies, cookie_path)

        if 'Set-Cookie'in page.headers.keys():

            header_set_cookie(page.headers['Set-Cookie'],cookie_path)

    return page


def poster(url,data, header_string,cookie_path ="",proxy = "",timeout = 20,show_cookie_setting = False):
    normal_header_string = header_string
    normal_header = get_header_dict(normal_header_string)
    verify_sta = 0
    if proxy != "":
        proxy = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy,
        }
        verify_sta = False

    if cookie_path == "":

        page = requests.post(url,data,headers=normal_header,proxies=proxy,verify=verify_sta,timeout = timeout)
    else:
        cookieg = load_cookies(cookie_path)
        #print (cookieg)
        page = requests.post(url,data, headers=normal_header, cookies=cookieg,proxies=proxy,verify=verify_sta,timeout = timeout)

        #page.cookies.update(cookieg)

        for bb in page.cookies:

            if show_cookie_setting == True:
                print(bb.name+":"+str(bb.value))

            edit_cookie(cookie_path,bb.name,bb.value)
        #save_cookies(page.cookies, cookie_path)

        if 'Set-Cookie'in page.headers.keys():

            header_set_cookie(page.headers['Set-Cookie'],cookie_path)

    return page

def edit_cookie(cookie_path,key,name):
    cookie = load_cookies(cookie_path)
    dr = requests.utils.dict_from_cookiejar(cookie)
    dr[key] = name
    ck = requests.utils.cookiejar_from_dict(dr)
    save_cookies(ck, cookie_path)
    #return cookie

def sendGmailSmtp(strGmailUser,strGmailPassword,strRecipient,strSubject,strContent):
    sender = strGmailUser
    receivers = [strRecipient]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(strContent, 'plain', 'utf-8')
    message['From'] = Header(strSubject, 'utf-8')
    message['To'] = Header(strRecipient, 'utf-8')

    subject = strSubject
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(strGmailUser,strGmailPassword)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
        smtpObj.close()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return 'send successed'

def send_notice_mail(title,data):
    email_acc = "junkerhelper@gmail.com"
    email_pwd = "12457868"
    geter_email = "junkerman4@gmail.com"

    title = "自動化系統通知:"+title

    sendGmailSmtp(email_acc,email_pwd,geter_email,title, data)


#倒數計時
class countdown (threading.Thread):
    def __init__(self,  time):
        threading.Thread.__init__(self)

        self.time = time

    def run(self):
        b = 0

        while b < self.time:

            z = self.time - b

            # print(db.get_time()+":倒數 "+format(z)+" 秒")
            time.sleep(1)
            b= b+1


        #print ("退出线程：" + self.name)

def emu_sleep(timer):
    # print(db.get_time()+":等待"+str(timer)+"秒後開始進行")
    thread_countdown = countdown(timer)
    thread_countdown.start()
    thread_countdown.join()
