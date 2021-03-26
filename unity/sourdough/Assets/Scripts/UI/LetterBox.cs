using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class LetterBox : MonoBehaviour
{
    public TMP_Text Letter;
    public GameObject Background;
    private bool OnFire;
    private Color BackgroundColor;
    private Color AlphaColor;
    private float FireTime = 6.0F;
    private float AlphaSpeed = .7f;
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        var renderer = this.gameObject.GetComponent<MeshRenderer>();

        if (OnFire && renderer.material.color.a > 0)
        {
            renderer.material.color = Color.Lerp(renderer.material.color, Color.clear, this.AlphaSpeed * 2  * Time.deltaTime);
            renderer = this.Background.GetComponent<MeshRenderer>();
            renderer.material.color = Color.Lerp(renderer.material.color, Color.clear, this.AlphaSpeed * Time.deltaTime);
            Letter.color = Color.Lerp(Letter.color, Color.clear, this.AlphaSpeed * Time.deltaTime);
        }
    }
    public void SetColor(Color c)
    {
        if (OnFire)
        {
            return;
        }
        var r = this.Background.GetComponent<Renderer>();
        r.material.SetColor("_Color", c);
    }
   
    public void Drop(bool destroy=false)
    {
        var body = this.GetComponent<Rigidbody>();
        body.isKinematic = false;
        body.useGravity = true;
        body.AddForce(new Vector3(Random.Range(-5, 5.0f), Random.Range(-5, 5.0f)));
        body.AddTorque(Random.Range(-10, 10.0f) * Vector3.one);
        if (destroy)
        {
            Destroy(this.gameObject, this.FireTime);
        }
        Debug.Log(this.FireTime);
        this.OnFire = true;
    }

    
}
