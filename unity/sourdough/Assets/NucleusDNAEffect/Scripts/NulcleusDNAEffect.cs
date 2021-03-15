using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class FloatRange
{
    public float Min;
    public float Max;
    public FloatRange(float min, float max)
    {
        this.Max = max;
        this.Min = min;
    }
}

public class NulcleusDNAEffect : MonoBehaviour {
    public int DNACount = 50;
    public GameObject DNAObject;
    public FloatRange XRange = new FloatRange(-2,-2);
    public FloatRange YRange = new FloatRange(-2, -2);
    public FloatRange ZRange = new FloatRange(0, 6);
    public FloatRange ScaleRange = new FloatRange(.005f, .025f);


    GameObject[] DNAs;
	// Use this for initialization

    float RandomRange(FloatRange range)
    {
        return Random.Range(range.Min, range.Max);
    }

	void Start () {
        DNAs = new GameObject[DNACount];

        for(int i=0;i<DNACount;i++)
        {
            Vector3 pos = new Vector3(RandomRange(this.XRange),
                RandomRange(this.YRange),
                RandomRange(this.ZRange));

            GameObject go = Instantiate(DNAObject);
            go.transform.position = pos;
            go.transform.rotation = Quaternion.Euler(Random.value * 360f, Random.value * 360f, Random.value * 360f);
            float scale = RandomRange(this.ScaleRange);
            go.transform.localScale = Vector3.one * scale;
            DNAs[i] = go;
        }
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
