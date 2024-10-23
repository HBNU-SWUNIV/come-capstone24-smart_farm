using System;
using System.Collections;
using System.Globalization;
using System.Text;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using uPLibrary.Networking.M2Mqtt.Messages;

public class Buttons : MonoBehaviour
{
    public TextMeshProUGUI txtRecv;
    public TextMeshProUGUI msg;
    CultureInfo cultureInfo;
    DateTime now;
    public M2MQTT m2mqtt;
    public Button btn;

    void Start()
    {
        m2mqtt = FindObjectOfType<M2MQTT>();
        cultureInfo = new CultureInfo("en-US");
    }

    public void OnClickSendData()
    {
        NowTime();
        string sendData = "";
        if(btn.name.Contains("LightOn")){
            sendData = "LightOn";
            msg.text = msg.text + "LightOn\n";
        }
        if(btn.name.Contains("LightOff")){
            sendData = "LightOff";
            msg.text = msg.text + "LightOff\n";
        }
        if(btn.name.Contains("SprinklerOn")){
            sendData = "SprinklerOn";
            msg.text = msg.text + "SprinklerOn\n";
            CancelInvoke("DisableObject");
            Invoke("EnableObject", 2f);
        }
        if(btn.name.Contains("SprinklerOff")){
            sendData = "SprinklerOff";
            msg.text = msg.text + "SprinklerOff\n";
            CancelInvoke("EnableObject");
            Invoke("DisableObject", 2f);
        }
        if(btn.name.Contains("ShutterOpen")){
            sendData = "ShutterOpen";
            msg.text = msg.text + "ShutterOpen\n";
        }
        if(btn.name.Contains("ShutterStop")){
            sendData = "ShutterStop";
            msg.text = msg.text + "ShutterStop\n";
        }
        if(btn.name.Contains("ShutterClose")){
            sendData = "ShutterClose";
            msg.text = msg.text + "ShutterClose\n";
        }


        if (m2mqtt != null && m2mqtt.client.IsConnected)
        {
            m2mqtt.client.Publish("Control", Encoding.UTF8.GetBytes(sendData), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
        }
        else
        {
            Debug.LogError("MQTT client is not connected");
        }
    }
    private void NowTime(){
        now = DateTime.Now;
        msg.text = msg.text + now.ToString("tt hh:mm:ss - ", cultureInfo);
    }
}
