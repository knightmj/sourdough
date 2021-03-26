using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class Award : MonoBehaviour
{
    public Image Image;
    public Text TitleText;
    public Text NameText;

    // Use this for initialization
    void Start()
    {

    }

    public void SetAward(string title, string name, string image, Color color)
    {
        this.TitleText.text = title;
        this.NameText.text = name;
        this.Image.sprite = Resources.Load<Sprite>(image);
        this.GetComponent<Image>().color = color;
    }


    // Update is called once per frame
    void Update()
    {

    }
}
