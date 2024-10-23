using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using TMPro;

public class M2MQTT : MonoBehaviour
{
    CultureInfo cultureInfo;
    DateTime now;
    public TextMeshProUGUI txtRecv;
    public MqttClient client;
    public List<string> receivedMessage = new List<string>(8);

    private const string MQTT_BROKER_ADDRESS = "127.0.0.1"; // 로컬 MQTT 브로커 주소
    private const int MQTT_BROKER_PORT = 1883; // MQTT 기본 포트

    void Start()
    {
        cultureInfo = new CultureInfo("en-US");
        try
        {
            client = new MqttClient(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, false, null, null, MqttSslProtocols.None);

            string clientId = Guid.NewGuid().ToString();
            client.Connect(clientId);

            if (client.IsConnected)
            {
                Debug.Log("MQTT connected");
                NowTime();
                txtRecv.text = txtRecv.text + "MQTT connected\n";
            }
            else
            {
                Debug.LogError("MQTT connection failed");
                NowTime();
                txtRecv.text = txtRecv.text + "MQTT connected failed\n";
            }

            client.Subscribe(new string[] { "sensor/+" }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
            client.MqttMsgPublishReceived += Client_MqttMsgPublishReceived;
        }
        catch (Exception ex)
        {
            Debug.LogError("MQTT connection error: " + ex.Message);
            NowTime();
            txtRecv.text = txtRecv.text + "MQTT connection error: " + ex.Message + "\n";
        }
    }

    void OnDestroy()
    {
        if (client != null && client.IsConnected)
        {
            client.Disconnect();
            Debug.Log("MQTT disconnected");
            NowTime();
            txtRecv.text = txtRecv.text + "MQTT disconnected\n";
        }
    }

    private void Client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
    {
        string message = Encoding.UTF8.GetString(e.Message);

        ClearList();
        receivedMessage.Add(message);
    }

    private void ClearList()
    {
        if (receivedMessage.Count >= receivedMessage.Capacity)
        {
            receivedMessage.Clear();
        }
    }
    private void NowTime(){
        now = DateTime.Now;
        txtRecv.text = txtRecv.text + now.ToString("tt hh:mm:ss - ", cultureInfo);
    }
}
