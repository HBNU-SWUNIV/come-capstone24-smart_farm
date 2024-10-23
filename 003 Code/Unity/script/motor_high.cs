using TMPro;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;

public class motor_high : MonoBehaviour
{
    public TextMeshProUGUI txtRecv;
    public GameObject myObject;
    private M2MQTT m2mqtt;

    private Vector3 targetPosition;
    private bool isMoving = false;

    void Start()
    {
        m2mqtt = FindObjectOfType<M2MQTT>();
        targetPosition = myObject.transform.position;
    }

    void Update()
    {
        if (m2mqtt.client.IsConnected)
        {
            ClearText();
            if (m2mqtt.receivedMessage.Count >= m2mqtt.receivedMessage.Capacity)
            {
                float newY = -4.803845f;
                float shutterValue = float.Parse(m2mqtt.receivedMessage[6]);

                if (shutterValue == 0.0f)
                {
                    txtRecv.text = "Shutter: 0%";
                    newY = -4.803845f;
                }
                else if (shutterValue == 1.0f)
                {
                    txtRecv.text = "Shutter: 25%";
                    newY = -4.603845f;
                }
                else if (shutterValue == 2.0f)
                {
                    txtRecv.text = "Shutter: 50%";
                    newY = -4.403845f;
                }
                else if (shutterValue == 3.0f)
                {
                    txtRecv.text = "Shutter: 75%";
                    newY = -4.203845f;
                }
                else if (shutterValue == 4.0f)
                {
                    txtRecv.text = "Shutter: 100%";
                    newY = -4.003845f;
                }

                targetPosition = new Vector3(0.8233576f, newY, 35.09001f);
                if (!isMoving)
                {
                    StartCoroutine(MoveObject(myObject.transform.position, targetPosition, 1.0f)); // 1.0f는 이동 시간
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

    private IEnumerator MoveObject(Vector3 start, Vector3 end, float duration)
    {
        isMoving = true;
        float elapsed = 0.0f;

        while (elapsed < duration)
        {
            myObject.transform.position = Vector3.Lerp(start, end, elapsed / duration);
            elapsed += Time.deltaTime;
            yield return null;
        }

        myObject.transform.position = end;
        isMoving = false;
    }
}
