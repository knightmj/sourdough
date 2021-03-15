using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class LetterBox : MonoBehaviour
{
    public TMP_Text Letter;
    public GameObject Background;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void SetColor(Color c)
    {
        var r = this.Background.GetComponent<Renderer>();
        r.material.SetColor("_Color", c);
    }
    public void Drop()
    {
        var body = this.GetComponent<Rigidbody>();
        body.isKinematic = false;
        body.useGravity = true;
    }
}
