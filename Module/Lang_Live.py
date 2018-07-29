import requests
from Module import net_fn
import json


class Lang_Live:

    def __init__(self):

        self.Host_List = []
        #用戶榜
        self.Rich_Month_Rank = []
        self.Rich_Week_Rank = []
        self.Rich_Daily_Rank = []


        #主播榜
        self.Host_Last_Hour_Potential_Rank = []
        self.Host_Last_Hour_Hot_Rank = []
        self.Host_Potential_Rank = []
        self.Host_Hot_Rank = []

        #主播 日 、月 、 週 榜
        self.Host_Dally_Rank = []
        self.Host_Month_Rank = []
        self.Host_Week_Rank = []

        #陽光榜
        self.Sun_Daily_Rank = []
        self.Sun_Month_Rank = []
        self.Host_Week_Rank = []

    def Init_Data(self):
        self.Get_Host_List()
        self.Get_Player_Rank()
        self.Get_Sun_Rank_All()
        self.Get_RealTime_Host_Rank()


    def Get_Host_List(self):
        url = "https://tw.api.langlive.com/v3/home/hot"
        header = "LOCALE: TW###USER-TOKEN: d292b71eb978881af434b0b10c76371b###USER-UID: 3101521###API-VERSION: 2.0###VERSION-CODE: 634###VERSION: 3.2.1.7###PLATFORM: Android###USER-MPHONE-BRAND: samsung###USER-MPHONE-OS-VER: 5.1.1###USER-MPHONE-MODELS: SM-G935K###Content-Type: application/x-www-form-urlencoded###Content-Length: 12###Host: tw.api.langlive.com###Connection: Keep-Alive###Accept-Encoding: gzip###User-Agent: okhttp/3.9.1"
        post_data = "sex=0&type=0"

        rs = net_fn.poster(url,header_string=header,data=post_data)
        data = rs.content.decode()
        data = json.loads(data)
        end = []
        for item in data['data']:
            if item['type'] != 4:
                continue

            hosts_list = item['list']
            for host_unit in hosts_list:
                if 'c_type' in host_unit and host_unit['c_type'] == 2:

                    for cells_item in host_unit['c_cells']:
                        end.append(cells_item)
                else:
                    end.append(host_unit)

        self.Host_List = end
        return end



    def Host_Fans_Rank(self,Host_id):
        url = "https://tw.api.langlive.com/v2/consume/top_send"
        header_string = "Host: tw.api.langlive.com###Connection: keep-alive###Content-Length: 36###Pragma: no-cache###Cache-Control: no-cache###Accept: application/json, text/javascript, */*; q=0.01###Origin: https://web.langlive.com###User-Agent: Mozilla/5.0 (Linux; Android 5.1.1; SM-G935K Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 langlive###Content-Type: application/x-www-form-urlencoded; charset=UTF-8###Accept-Encoding: gzip, deflate###Accept-Language: zh-TW,en-US;q=0.8###X-Requested-With: com.lang.lang"
        post_data = "stamp=0&len=50&action=0&pfid="+format(Host_id)
        rs = net_fn.poster(url,data=post_data,header_string=header_string)
        data = rs.content.decode()
        return json.loads(data)



    def Get_Player_Rank(self):
        url = "https://tw.api.langlive.com/html/ranklist"
        header_string = "Host: tw.api.langlive.com###Connection: keep-alive###Content-Length: 34###Pragma: no-cache###Cache-Control: no-cache###Accept: application/json, text/javascript, */*; q=0.01###Origin: https://web.langlive.com###User-Agent: Mozilla/5.0 (Linux; Android 5.1.1; SM-G935K Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 langlive###Content-Type: application/x-www-form-urlencoded; charset=UTF-8###Accept-Encoding: gzip, deflate###Accept-Language: zh-TW,en-US;q=0.8###X-Requested-With: com.lang.lang"

        post_data = "rank_id=0&stamp=0&len=50&include=0"

        rs = net_fn.poster(url,header_string=header_string,data=post_data)
        data = rs.content.decode()
        data = json.loads(data)
        self.Rich_Month_Rank = data['rich_month']
        self.Rich_Week_Rank = data['rich_week']
        self.Rich_Daily_Rank = data['rich_daily']


    def Get_Sun_Rank_All(self):
        self.Sun_Daily_Rank = self.Get_Sun_Rank(2)
        self.Sun_Month_Rank =  self.Get_Sun_Rank(3)
        self.Host_Week_Rank =  self.Get_Sun_Rank(4)



    def Get_Sun_Rank(self,Rank_Type):
        url = "https://tw.api.langlive.com/v2/html/sun_task/receive_rank"
        header_str = "Host: tw.api.langlive.com###Connection: keep-alive###Content-Length: 11###Pragma: no-cache###Cache-Control: no-cache###Accept: application/json, text/javascript, */*; q=0.01###Origin: https://web.langlive.com###User-Agent: Mozilla/5.0 (Linux; Android 5.1.1; SM-G935K Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 langlive###Content-Type: application/x-www-form-urlencoded; charset=UTF-8###RAccept-Encoding: gzip, deflate###Accept-Language: zh-TW,en-US;q=0.8###X-Requested-With: com.lang.lang"
        post_data = "rank_type="+format(Rank_Type)

        rs = net_fn.poster(url,header_string=header_str,data=post_data)
        data = rs.content.decode()
        data = json.loads(data)

        return data


    def Get_RealTime_Host_Rank(self):
        url = "https://tw.api.langlive.com/v2/html/realtime/rank_list_3?anchor_pfid=1269640"
        header_string = "Host: tw.api.langlive.com###Connection: keep-alive###Content-Length: 0###Pragma: no-cache###Cache-Control: no-cache###Accept: application/json, text/plain, */*###Origin: https://web.langlive.com###User-Agent: Mozilla/5.0 (Linux; Android 5.1.1; SM-G935K Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 langlive###Referer: https://web.langlive.com/html/realTimeRank/realTimeRank.html?anchor_pfid=1269640&HTTP_USER_UID=3101521&HTTP_USER_TOKEN=d292b71eb978881af434b0b10c76371b###Accept-Encoding: gzip, deflate###Accept-Language: zh-TW,en-US;q=0.8###X-Requested-With: com.lang.lang"
        rs = net_fn.poster(url,header_string=header_string,data="")
        data = rs.content.decode()
        data = json.loads(data)

        self.Host_Last_Hour_Potential_Rank = data['data']['last_hour_list_1']
        self.Host_Last_Hour_Hot_Rank = data['data']['last_hour_list_2']
        self.Host_Potential_Rank = data['data']['hour_list_1']
        self.Host_Hot_Rank = data['data']['hour_list_2']

        # print(self.Hot_Rank)

        #last_hour_list_1
        #上小時潛力榜
        #last_hour_list_2
        #上小時當紅榜
        #hour_list_1
        #潛力榜
        #hour_list_2
        #當紅榜



if __name__ == '__main__':
    obj = Lang_Live()
    # obj.Get_Rank()
    rs = obj.Host_Fans_Rank('2316609')
    print(rs)
    # obj.Get_Host_List()