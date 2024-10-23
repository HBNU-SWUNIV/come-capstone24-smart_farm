using TMPro;
using UnityEngine;
using System;

public class LightMat : MonoBehaviour
{
    public Material[] mat = new Material[2];
    public TextMeshProUGUI txtRecv;


    void Start()
    {
    }

    void Update()
    {
        if(txtRecv.text.Contains("ON")){
            gameObject.GetComponent<MeshRenderer>().material = mat[0];
        }
        else if(txtRecv.text.Contains("OFF")){
            gameObject.GetComponent<MeshRenderer>().material = mat[1];
        }
    }
}