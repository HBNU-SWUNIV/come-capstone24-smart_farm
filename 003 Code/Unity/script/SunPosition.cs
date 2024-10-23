using System;
using UnityEngine;

public class SunPosition : MonoBehaviour
{

        public Light directionalLight;
        private float RotationH = 0;
        private float AngleH = 15;
        private float RotationM = 0;
        private float AngleM = 0.25f;
        private float Rotation = 0;
        int StandardHour = 6;

        void Start()
        {
            int utcNow = DateTime.UtcNow.Hour;

            int NowHour = utcNow + 9;
            int NowMinute = DateTime.Now.Minute;
            if (NowHour - 6 < 0)
            {
                RotationH = (NowHour + 24 - StandardHour) * AngleH;
            }
            else
            {
                RotationH = (NowHour - 6) * AngleH;
            }
            RotationM = NowMinute * AngleM;
            Rotation = RotationH + RotationM;
            directionalLight.transform.localRotation = Quaternion.Euler(Rotation, 0, 0);
            // StartCoroutine(LightRotate());
        }

        // IEnumerator LightRotate()
        // {
        //     while (true)
        //     {
        //         Rotation += 2.5f;
        //         directionalLight.transform.localRotation = Quaternion.Euler(Rotation, 0, 0);
        //         yield return new WaitForSecondsRealtime(600);
        //     }

        // }

    }