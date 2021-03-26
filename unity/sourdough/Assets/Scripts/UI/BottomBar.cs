using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class BottomBar : MonoBehaviour
{
    public InputField WordInputField;
    public Text PlayerNameText;
    public Text StatusText;
    public GameObject HintText;
    public Text ValidWordsText;
    public Text InvalidWordsText;
    public HashSet<string> KnownWords = new HashSet<string>();
    public List<GameObject> AddedText = new List<GameObject>();
    public string PayerName;
    // Start is called efore the first frame update
    void Start()
    {
        StatusText.text = "";
        ValidWordsText.text = "";
        InvalidWordsText.text = "";

    }
    IEnumerator FlashStatus(string text)
    {
        StatusText.text = text;
        yield return new WaitForSeconds(2);
        StatusText.text = "";
    }
    public void SetStatus(string status)
    {
        StartCoroutine(FlashStatus(status));
    }

    public void Reset()
    {
        foreach(var go in this.AddedText)
        {
            Destroy(go);
        }
        this.AddedText.Clear();
        this.KnownWords.Clear();
        ValidWordsText.text = "";
        InvalidWordsText.text = "";
    }

    public void UpdateState(GameState gameState)
    {
        var tmp = HintText.GetComponent<TextMeshProUGUI>();
        tmp.text = gameState.RuleText;

        int myValid = 0;
        int myInvaid = 0;
        foreach(var word in gameState.Words)
        {
            if (word.PlayerName == this.PayerName)
            {
                if (word.Valid)
                    myValid++;
                else
                    myInvaid++;
            }
            if (!KnownWords.Contains(word.Text))
            {
                KnownWords.Add(word.Text);
             
                if (word.Valid)
                {
                    ValidWordsText.text = word.Text + " " + ValidWordsText.text;
                }
                else
                {
                    InvalidWordsText.text = word.Text + " " + InvalidWordsText.text;
                }
            }
        }
        PlayerNameText.text = this.PayerName + " <color=#388A3E>" + myValid + "</color>/<color=#D37F31>" + myInvaid + "</color>";
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
