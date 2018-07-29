using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using WebSocketSharp;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Diagnostics;
using System.Windows.Threading;
using System.Threading;
using System.Collections.ObjectModel;

namespace Lang_Spider_UI
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            WS_Init();
        }


        public class Rank_Unit_Pack
        {
            public string name { get; set; }
            public string pfid { get; set; }
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Send_Order("Renew_RealTime_Rank","");
        }


        public void Update_Rank_Pack (DataGrid Main_Grid, JArray Data_List) {

            var Data_Grid_List = new ObservableCollection<Rank_Unit_Pack>();


            foreach (var item in Data_List)
            {
                var new_unit_item = new Rank_Unit_Pack();
                new_unit_item.name = (string)item["nickname"];
                new_unit_item.pfid = (string)item["pfid"];

                Data_Grid_List.Add(new_unit_item);


                // Console.WriteLine(item[""]);
            }
          
            Dispatcher.Invoke(DispatcherPriority.Normal,
                          new Action<DataGrid, ObservableCollection<Rank_Unit_Pack>>
                          (Change_DataGrid_Source), Main_Grid,Data_Grid_List);


        }

        public void Change_DataGrid_Source(DataGrid DG,ObservableCollection<Rank_Unit_Pack> source)
        {
            DG.ItemsSource = source;
        }


        //ws連線設定
        private WebSocket WS;
        const string host = "ws://127.0.0.1:9988";

        public void WS_Init()
        {


            WS = new WebSocket(host);

            WS.OnMessage += (ss, ee) =>
                Msg_Decode(ee.Data);
            
            WS.OnOpen += (ss, ee) =>
                 Onopen_fn(ss,ee);

            WS.OnError += (sender, e) => 
                On_Error_fn(sender, e);

            WS.OnClose += (sender, e) => 
                On_Close_fn(sender, e);

            WS.Connect();
        }

        
        private void Msg_Decode(string json)
        {
            try
            {
                dynamic data = JValue.Parse(json);
                string order = data["order"];
                var detail = data["detail"];
                switch (order)
                {
                    case "New_Realtime_Rank":

                        
                        Update_Rank_Pack(Last_Hour_P_Rank, detail["Host_Last_Hour_Potential_Rank"]);
                        Update_Rank_Pack(Last_Hour_H_Rank, detail["Host_Last_Hour_Hot_Rank"]);
                        Update_Rank_Pack(Rank_P_Total, detail["Host_Potential_Rank"]);
                        Update_Rank_Pack(Rank_H_Total, detail["Host_Hot_Rank"]);

                        break;

                    default:
                        Console.WriteLine(json);
                        break;
                }

            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                Console.WriteLine(json);
                Console.WriteLine("error_WS_Msg_not a JSON");
            }


        }



        private void Onopen_fn(object ss , EventArgs e)
        {
            Dispatcher.Invoke(
                        DispatcherPriority.Normal,
                        new Action<Label, string>(Change_Label_Text),
                        WS_Con_Stat, "已連線"
                        );
        }
        private void On_Close_fn(object ss, CloseEventArgs e)
        {
            Debug.WriteLine("WS_Close");
            Debug.WriteLine(WS.ReadyState);

            Dispatcher.Invoke(
                         DispatcherPriority.Normal,
                         new Action<Label, string>(Change_Label_Text),
                         WS_Con_Stat, "已斷線"
                         );


            //自動重連
            while (WS.ReadyState.ToString() == "Closed")
            {
                Thread.Sleep(1000);
                WS.Connect();

            }

        }

        private void Change_Label_Text(Label Lab, string txt)
        {
            Lab.Content = txt;
        }


        private void On_Error_fn(object ss, WebSocketSharp.ErrorEventArgs e)
        {
            Debug.WriteLine("WS_Error");
            Debug.WriteLine(e);

        }

        private void Send_Order(string order, dynamic detail)
        {
            JObject data = new JObject();
            data["order"] = order;
            data["detail"] = detail;

            string json = data.ToString(Formatting.None);

            WS.Send(json);
        }


    }
}
