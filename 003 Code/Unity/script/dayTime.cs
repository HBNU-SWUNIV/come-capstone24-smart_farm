using System;
using System.Globalization;
using TMPro;
using UnityEngine;

public class dayTime : MonoBehaviour
{
    public TextMeshProUGUI txtRecv;
    DateTime now;
    CultureInfo cultureInfo;

    void Start()
    {
        cultureInfo = new CultureInfo("en-US");
    }

    void Update()
    {
        now = DateTime.Now;
        txtRecv.text = now.ToString("yyyy-MM-dd hh:mm:ss tt", cultureInfo);
    }
}
