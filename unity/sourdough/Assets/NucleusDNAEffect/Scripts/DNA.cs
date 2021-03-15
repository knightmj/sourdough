﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DNA : MonoBehaviour {
    private ParticleSystem PS;
    private ParticleSystem.MainModule _psmm;

    float density = 20;
    float curve = -7;

    List<Vector3> dnaPoints = new List<Vector3>();


    // Use this for initialization
    void Start () {
        PS = GetComponent<ParticleSystem>();
        _psmm = PS.main;


        MakeDNA(Vector3.zero, 100f);
        MakeLadder(100f);
    }

    void MakeDNA(Vector3 position,float length)
    {
        float addp = 0;
        float height = 0;

        for (float p = 0; p < length * density; p++)
        {
            // create a particle with random
            height += 1 / density;
            float pX = 5;
            float pY = height + (Random.Range(-10f,10f) / 10f);
            float pZ = 0;

            Vector3 point = new Vector3();
            point.x = pX;

            Vector3 center = new Vector3();

            addp += 180 + (curve / density);

            Vector3 r = rotateAround(point, center, addp);
            addp %= 360;
            pX = r.x;
            pZ = r.y;

            dnaPoints.Add(new Vector3(pX, pY, pZ));
        }


    }

    void MakeLadder(float length)
    {
        float addp = 0;
        float height = 0;
        float ladderspace = 4;
        for (float p = 0; p <= length / ladderspace; p++)
        {
            // create a particle with random
            for (float i = 0; i < density * 2f; i++)
            {
                float pX = Random.Range(-50f, 50f) / 10f;
                float pY = height + (Random.Range(-4f, 4f) / 10f);
                float pZ = 0;

                Vector3 point = new Vector3();
                point.x = pX;

                Vector3 center = new Vector3();
                addp += 180f;

                Vector3 r = rotateAround(point, center, addp);
                addp %= 360;
                pX = r.x;
                pZ = r.y;

                dnaPoints.Add(new Vector3(pX, pY, pZ));
            }
            addp += curve * ladderspace;
            addp %= 360;
            height += ladderspace;
        }
    }

    Vector3 rotateAround(Vector3 point,Vector3 center,float angle)
    {
        angle = (angle) * (Mathf.PI / 180f); // Convert to radians
        float rotatedX = Mathf.Cos(angle) * (point.x - center.x) - Mathf.Sin(angle) * (point.y - center.y) + center.x;
        float rotatedY = Mathf.Sin(angle) * (point.x - center.x) + Mathf.Cos(angle) * (point.y - center.y) + center.y;

        return new Vector3(rotatedX, rotatedY);
    }


    // Update is called once per frame
    void Update () {

        ParticleSystem.Particle[] ps = new ParticleSystem.Particle[PS.particleCount];
        int pCount = PS.GetParticles(ps);

        for (int i = 0; i < dnaPoints.Count; i++)
        {
            if (i < pCount)
            {
                Vector3 pos = dnaPoints[i];

                ps[i].position = pos;
            }
        }

        PS.SetParticles(ps, pCount);


        transform.Rotate(new Vector3(0.0f, 0.0f, 0.1f));

        //transform.position = pos1;

    }
}
