using TMPro;
using UnityEngine;
using System;

public class Texts : MonoBehaviour
{
    public TextMeshProUGUI txtRecv;

    private M2MQTT m2mqtt;

    void Start()
    {
        m2mqtt = FindObjectOfType<M2MQTT>();
    }

    void Update()
    {
        if (m2mqtt.client.IsConnected)
        {
            ClearText();
            /*  0 = 내부온도
                1 = 내부습도
                2 = 외부온도
                3 = 외부습도
                4 = 조도
                5 = 토양습도
                6 = 유량계
                7 = 모터1
                8 = 모터2 
            */
            if (m2mqtt.receivedMessage.Count >= m2mqtt.receivedMessage.Capacity)
            {
                if(txtRecv.name.Contains("TempTxt"))
                {
                    txtRecv.text = "Temp: " + m2mqtt.receivedMessage[0] + "C / " + m2mqtt.receivedMessage[2] + "C";
                }
                if(txtRecv.name.Contains("HumiTxt"))
                {
                    txtRecv.text = "Humi: " + m2mqtt.receivedMessage[1] + "% / " + m2mqtt.receivedMessage[3] + "%";
                }
                if(txtRecv.name.Contains("LightTxt"))
                {
                    if(float.Parse(m2mqtt.receivedMessage[4]) > 1000.0 && float.Parse(m2mqtt.receivedMessage[4]) < 1200.0){
                        txtRecv.text = "Light: ON";
                    }
                    else{
                        txtRecv.text = "Light: OFF";
                    }
                }
                if(txtRecv.name.Contains("SprinklerTxt")){
                    
                }
                if(txtRecv.name.Contains("SoilTxt")){
                    if(float.Parse(m2mqtt.receivedMessage[5]) > 430.0){
                        txtRecv.text = "Soil Moisture: Dry";
                    }
                    else if(float.Parse(m2mqtt.receivedMessage[5]) > 330.0){
                        txtRecv.text = "Soil Moisture: Wet";
                    }
                    else if(float.Parse(m2mqtt.receivedMessage[5]) > 260.0){
                        txtRecv.text = "Soil Moisture: Very Wet";
                    }
                }
                if(txtRecv.name.Contains("MoterTxt")){
                    if(float.Parse(m2mqtt.receivedMessage[7]) > 500.0){
                        txtRecv.text = "Left Motor : On";
                    }
                    else if(float.Parse(m2mqtt.receivedMessage[7]) < 500.0){
                        txtRecv.text = "Left Motor : Off";
                    }
                    else if(float.Parse(m2mqtt.receivedMessage[8]) > 500.0){
                        txtRecv.text = "Right Motor : On";
                    }
                    else if(float.Parse(m2mqtt.receivedMessage[8]) < 500.0){
                        txtRecv.text = "Right Motor : Off";
                    }
                }
            }
        }
    }

    private void ClearText()
    {
        if (txtRecv.textInfo.lineCount >= m2mqtt.receivedMessage.Capacity)
        {
            txtRecv.text = "";
        }
    }
}