using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI
;

public class NameStatus : MonoBehaviour
{
    public Text Text;
    public Text StatusText;
    int lastValid = 0;
    int lastInvalid = 0;
    void Start()
    {
        StatusText.text = "";
    }
    IEnumerator FlashNew(string text)
    {
        StatusText.text = text;
        yield return new WaitForSeconds(2);
        StatusText.text = "";
    }
    public void SetStatus(string player, int valid, int invalid)
    {
        Text.text = player + " <color=#388A3E>" + valid + "</color>/<color=#D37F31>" + invalid + "</color>";
        if (valid != this.lastValid)
        {
            StartCoroutine(FlashNew("<color=#388A3E>+" + (valid - lastValid) + "</color>"));
        }
        else if (invalid != this.lastInvalid)
        {
            StartCoroutine(FlashNew("<color=#D37F31>+" + (invalid - lastInvalid) + "</color>"));
        }
        lastInvalid = invalid;
        lastValid = valid;
    }
}
