# coding=utf-8

import requests
from Module import net_fn
from Control import Spider_Control
import time
import codecs
from Module import  wui

class Main:
    def __init__(self):
        self.Wui = wui.WUI("","",exit_time=999999,port=9988)
        self.Spider = Spider_Control.Spider(wui=self.Wui)
        self.WS_Hook()
        self.Wui.Start_WS(start_browser=0)





        # self.Spider.Get_All_Host_Rank()
    def WS_Hook(self):
        self.Wui.Add_Recv_Msg_Hook("Renew_RealTime_Rank",self.Spider.Renew_RealTime_Rank_fn)
    def Export_CSV(self):
        Host_Rank_Data = self.Spider.Host_Rank_Data

        csv_all = ""
        for pfid in Host_Rank_Data:
            data = Host_Rank_Data[pfid]

            Rank_List = data['Rank_List']

            if 'name' not in data['jump']:
               continue


            row_1 = "{}".format(data['jump']['name'])
            row_2 = "{}".format(pfid)


            if 'total_list' not in Rank_List:
                Total_List = Rank_List['week_list']['list']
            else:
                Total_List = Rank_List['total_list']['list']

            for Player_Item in Total_List:
                nickname = Player_Item['nickname']
                row_1 += ",{}".format(nickname)
                row_2 += ",{}".format(Player_Item['total'])

            # print(row_1)
            # print(row_2)
            csv_all += row_1+"\n"
            csv_all += row_2+"\n"

            # print(Total_List)
            # print(row_2)
        csv_all = csv_all
        # csv_all = csv_all.decode("big5")
        fp = open("export.csv",'w+',encoding='utf-8')
        fp.write('\ufeff')
        fp.write(csv_all)
        fp.close()

    def Export_Host_Total(self):
        Host_Rank_Data = self.Spider.Host_Rank_Data

        csv_all = ""
        for pfid in Host_Rank_Data:
            data = Host_Rank_Data[pfid]

            Rank_List = data['Rank_List']

            if 'name' not in data['jump']:
                continue

            row_1 = "{},{}".format(pfid,data['jump']['name'])
            # row_2 = "{}".format(pfid)

            Total_Money = 0

            if 'total_list' not in Rank_List:
                Total_List = Rank_List['week_list']['list']
            else:
                Total_List = Rank_List['total_list']['list']

            for Player_Item in Total_List:
                nickname = Player_Item['nickname']

                Total_Money += int(Player_Item['total'])

            row_1 += ","+str(Total_Money)


            csv_all += row_1 + "\n"

            # print(Total_List)
            # print(row_2)

        csv_all = csv_all
        # csv_all = csv_all.decode("big5")
        fp = open("export_total_money.csv", 'w+', encoding='utf-8')
        fp.write('\ufeff')
        fp.write(csv_all)
        fp.close()

if __name__ == '__main__':
    obj = Main()
    obj.Export_Host_Total()
