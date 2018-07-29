from Module import Lang_Live
from tqdm import tqdm
from threading import Thread
from queue import Queue
import time
import json


class Spider:
    def __init__(self):
        self.Lang_Obj = Lang_Live.Lang_Live()
        self.Lang_Obj.Init_Data()
        self.Queue = Queue()
        self.Host_Rank_Data = {}


    def Get_All_Host_Rank(self):
        All_Host_List = self.Lang_Obj.Host_List

        for item in All_Host_List:
            pfid = item['jump']['pfid']
            self.Host_Rank_Data[str(pfid)] = item
            self.Queue.put(pfid)

        self.Run_Host_Rank_Thread()

        start_time = time.time()
        print("開始抓取主播粉絲榜")
        while self.Queue.qsize() > 0:
            time.sleep(0.2)
        #讓最後一個任務運作完成
        time.sleep(3)

        af_time = time.time() - start_time

        # print(json.dumps(self.Lang_Obj.Host_List[len(self.Lang_Obj.Host_List)-1]))
        # print(self.pfid_Index["1218368"])

        print("工作完成，耗時{}秒".format(af_time))

    def Host_Rank_Thread(self):
        while self.Queue.qsize() > 0:
            pfid = self.Queue.get()
            Rank_List = self.Lang_Obj.Host_Fans_Rank(pfid)

            self.Host_Rank_Data[str(pfid)]['Rank_List'] = Rank_List
            # print(self.pfid_Index[str(pfid)])

            time.sleep(0.2)



    def Run_Host_Rank_Thread(self):
        Max_Num = 30
        for n in range(Max_Num):
            th = Thread(target=self.Host_Rank_Thread)
            th.start()




if __name__ == '__main__':
    obj = Spider()
    # obj.Get_All_Host_Rank()

