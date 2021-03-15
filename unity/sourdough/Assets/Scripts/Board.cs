using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; 


public class Board : MonoBehaviour
{
    public GameObject LetterPrefab;
    public InputField wordTextField;
    private string[][] boardData;
    private LetterBox[][] board;

    // Start is called before the first frame update
    void Start()
    {

        Action<string[][]> boardLoaded = board =>
        {
            this.boardData = board;
            this.CreateBoard();
        };
        Action<string> boardLoadError = error =>
        {
            Debug.LogError(error);
        };

        var server = this.GetComponent<GamerServer>();
        StartCoroutine(server.LoadBoard("island_adverbia", boardLoaded, boardLoadError));

    }

    public void CreateBoard()
    {
        Bounds b = LetterPrefab.GetComponent<MeshFilter>().sharedMesh.bounds;
        this.board = new LetterBox[this.boardData.Length][];

        for (int r = 0; r < boardData.Length; r++)
        {
            this.board[r] = new LetterBox[boardData[r].Length];

            for (int c = 0; c < boardData[r].Length; c++)
            {
                GameObject go = GameObject.Instantiate(LetterPrefab, this.transform);
                go.transform.position = new Vector3(
                    (c * b.size.x * this.transform.localScale.x) - (.5f * boardData[0].Length * b.size.x * this.transform.localScale.x),
                    (-r * b.size.y * this.transform.localScale.y) + (.5f * boardData.Length * b.size.y * this.transform.localScale.y),
                    -1
                    );
                LetterBox lb = go.GetComponent<LetterBox>();
                lb.Letter.text = boardData[r][c];
                this.board[r][c] = lb;

                if (boardData[r][c] == " ")
                {
                    lb.Drop();
                }
            }
        }
    }
    public void AddWord()
    {
        
    }

    public void TextEntered(string text)
    {
        Debug.Log(this.wordTextField.text);
        if (Input.GetKeyUp(KeyCode.Return))
        {
            AddWord();
        }
        for (int r = 0; r < boardData.Length; r++)
        {
            for (int c = 0; c < boardData[r].Length; c++)
            {
                this.board[r][c].SetColor(Color.white);     
            }
        }
        if (this.wordTextField.text.Length == 0)
        {
            return;
        }
        Debug.Log(this.wordTextField.text);
        List<List<Point>> paths = PathFinder.GetActiveCells(
            this.wordTextField.text.ToUpper(), boardData);

        foreach (var path in paths)
        {
            Debug.Log(path.Count);
            int i = 0;
            foreach (var p in path)
            {
                float alpha = .10f + (1 / ((float)path.Count - i++));
                this.board[p.x][p.y].SetColor(new Color(200/255.0f,
                    70.0f/255.0f,
                    200.0f/255.0f,
                    alpha));
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
