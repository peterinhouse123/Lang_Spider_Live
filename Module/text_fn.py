# -*- coding: UTF-8 -*-
import re
import hashlib
import base64


def md5(string):
    m = hashlib.md5()
    string = string.encode('utf-8')
    # print(string)
    m.update(string)
    return m.hexdigest()


#用正則表達式取得文字
def preg_get_word(preg_word,num,text,mode = 0):

    try:


        patte = re.compile(preg_word)
        grk = patte.search(text)

        if num =="all":
            bb = re.findall(preg_word,text)
            rs = bb
            if len(rs) ==0:
                rs ="empty_data"
        else:
            rs = grk.group(num)
            if mode == "test":

                print("正則表達式:"+preg_word+"\n 結果:"+rs.encode("utf-8"))

    except:
        rs = "empty_data"



    return rs

def encrypt(txt,key=''):
    if key == '':
        key = default_key
    cipher_suite = Fernet(key)
    if type(txt) == str:
        txt = txt.encode()
    cipher_text = cipher_suite.encrypt(txt)
    return cipher_text

def decrypt(txt,key=''):
    if key == '':
        key = default_key

    cipher_suite = Fernet(key)
    rs = cipher_suite.decrypt(txt)

    return rs


if __name__ == '__main__':

        cr = "adskfj;zxcv;lknbzx.c,mvn/ksdflj;asklf'zcxbvnzkmvcx,.vnzx'cvja';sldkfapiosjvonzmxlkcbnasdm,f"

        gz = encrypt(cr)
        print(gz)
        print(decrypt(gz))


        # key = Fernet.generate_key()

        # cipher_suite = Fernet(key)
        # cipher_text = cipher_suite.encrypt(cr.encode())
        # print(cipher_text)
        # print(type(cipher_text))
        # plain_text = cipher_suite.decrypt(cipher_text)
        # print(plain_text)