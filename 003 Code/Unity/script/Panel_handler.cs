using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DG.Tweening;

public class Panel_Handler : MonoBehaviour
{
   void Start()
   {      
      DOTween.Init();
      transform.localScale = Vector3.one * 0.1f;
      gameObject.SetActive(false);
   }

   public void Show()
   {
      gameObject.SetActive(true);

      var seq = DOTween.Sequence();

      seq.Append(transform.DOScale(1.1f, 0.2f));
      seq.Append(transform.DOScale(1f, 0.1f));

      seq.Play();
   }

   public void Hide()
   {
      var seq = DOTween.Sequence();

      transform.localScale = Vector3.one * 0.2f;

      seq.Append(transform.DOScale(1.1f, 0.1f));
      seq.Append(transform.DOScale(0.2f, 0.2f));

      seq.Play().OnComplete(() =>
      {
         gameObject.SetActive(false);
      });
   }
}