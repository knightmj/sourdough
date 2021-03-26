using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class FoundWord : MonoBehaviour
{
    public TextMeshPro word;
    public float direction = -1;
    // Start is called before the first frame update
    void Start()
    {
        
    }
    public static GameObject Create(string text, bool valid)
    {
        GameObject go = Instantiate(Resources.Load("Prefabs/FoundWord")) as GameObject;
        var foundWord = go.GetComponent<FoundWord>();
        foundWord.word.text = text;

        if (valid)
        {
            foundWord.word.color = new Color(0.219f, 0.541f, 0.243f);
            go.transform.position = new Vector3(
                 Random.Range(-7.0f, 7),
                 Random.Range(0, 3.5f),
                 1);
        }
        else
        {
            foundWord.word.color = new Color(0.827f, 0.498f, 0.192f);

            go.transform.position = new Vector3(
                       Random.Range(-7.0f, 7),
                       Random.Range(-3.5f, 0),
                 1);
                
        }
        go.transform.localScale = Vector3.one * Random.Range(.3f, .6f);
        var t = go.GetComponent<RectTransform>();
        t.Rotate(
           new Vector3(0, 0, Random.Range(-.1f,.2f)));
        if (Random.value < .5)
        {
            foundWord.direction *= -1;
        }
        return go;
    }

    // Update is called once per frame
    void Update()
    {
        var t = this.GetComponent<RectTransform>();
        if (Mathf.Abs(t.rotation.z) > 0.2f)
            this.direction *= -1;
        t.Rotate(
             new Vector3(0, 0, this.direction * .05f));
    }
}
