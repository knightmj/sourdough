using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Board : MonoBehaviour
{
    public GameObject LetterPrefab;
    public ScoreBoard TopScoreBoard;
    public BottomBar BottomBarCanvas;
    public SoundManager Sounds;
    public GameObject NameStatusPrefab;
    public GameObject Canvas;

    public string game = "mik3";
    public string player = "player";
    private bool debugMode = false;

    private int levelIndex = -1;
    private string[][] boardData;
    private LetterBox[][] board;

    private long lastGameUpdate;
    private Dictionary<string, GameObject> foundWordDictionary
        = new Dictionary<string, GameObject>();

    private Dictionary<string, GameObject> playersDictionary
    = new Dictionary<string, GameObject>();

    private bool clockStarted = false;

    // Start is called before the first frame update
    void Start()
    {
        if (debugMode)
        {
            BottomBarCanvas.PayerName = this.player;
            LoadBoard();
        }
        else
        {
            this.game = "";
            this.player = "";
        }
    }
    public void SetName(string playerName)
    {
        this.player = playerName;
        BottomBarCanvas.PayerName = this.player;
    }

    public bool StartGame(string gameName)
    {
        this.game = gameName;
        LoadBoard();
        return true;
    }
    private void LoadBoard()
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
        StartCoroutine(server.LoadBoard(this.game, boardLoaded, boardLoadError));

    }
    public void CreateBoard()
    {
        Bounds b = LetterPrefab.GetComponent<MeshFilter>().sharedMesh.bounds;
        float width = b.size.x * LetterPrefab.transform.localScale.x;
        float height = b.size.y * LetterPrefab.transform.localScale.y;

        this.board = new LetterBox[this.boardData.Length][];    

        for (int r = 0; r < boardData.Length; r++)
        {
            this.board[r] = new LetterBox[boardData[r].Length];

            for (int c = 0; c < boardData[r].Length; c++)
            {
                GameObject go = GameObject.Instantiate(LetterPrefab, this.transform);
                go.transform.position = new Vector3(
                    (c * width) - (.5f * boardData[0].Length * width) + .5f * width,
                    (-r * height) + (.5f * boardData.Length * height),
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
        Action<bool, bool, string> wordAdded = (error, isValid, message) =>
        {
            BottomBarCanvas.SetStatus(message);
            if (error)
            {
                Sounds.PlaySound(Sounds.knownWordAudioSource);
            }
            if (isValid)
            {
                Sounds.PlaySound(Sounds.validWordAudioSource);
            }
            else
            {
                Sounds.PlaySound(Sounds.invalidWordAudioSource);
                BottomBarCanvas.SetStatus(message);
            }
        };

        Action<string> onError = message => {
            Debug.Log(message);
            BottomBarCanvas.SetStatus(message);
        };

        var server = this.GetComponent<GamerServer>();
        StartCoroutine(server.AddWord(this.game, this.BottomBarCanvas.WordInputField.text, this.player, wordAdded, onError));
        this.BottomBarCanvas.WordInputField.text = "";
        this.BottomBarCanvas.WordInputField.ActivateInputField();
    }

    public void TextEntered(string text)
    {
        for (int r = 0; r < boardData.Length; r++)
        {
            for (int c = 0; c < boardData[r].Length; c++)
            {
                this.board[r][c].SetColor(Color.white);     
            }
        }
        if (this.BottomBarCanvas.WordInputField.text.Length == 0)
        {
            return;
        }
        if (Input.GetKeyDown(KeyCode.Return))
        {
            AddWord();
            return;
        }
        List<List<Point>> paths = PathFinder.GetActiveCells(
            this.BottomBarCanvas.WordInputField.text.ToUpper(), boardData);

        foreach (var path in paths)
        {
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
    public void ToggleMute()
    {
        Sounds.Mute = !Sounds.Mute;
    }

    IEnumerator WaitAndLoad()
    {
        yield return new WaitForSeconds(2);
        LoadBoard();
    }
    void NextBoard(int levelIndex)
    {
        this.levelIndex = levelIndex;
        for (int r = 0; r < boardData.Length; r++)
        {
            for (int c = 0; c < boardData[r].Length; c++)
            {
                this.board[r][c].Drop(true);
            }
        }
        foreach(var key in this.foundWordDictionary.Keys)
        {
            Destroy(this.foundWordDictionary[key]);
        }
        this.foundWordDictionary.Clear();
        foreach (var key in this.playersDictionary.Keys)
        {
            Destroy(this.playersDictionary[key]);
        }
        this.playersDictionary.Clear();

        Sounds.PlaySound(Sounds.levelUpAudioSource);

        this.foundWordDictionary.Clear();
        BottomBarCanvas.Reset();
        StartCoroutine(WaitAndLoad());
    }

    void UpdateWordsFound(GameState state)
    {
        foreach(var word in state.Words)
        {
            if (!this.foundWordDictionary.ContainsKey(word.Text))
            {
                var go = FoundWord.Create(word.Text, word.Valid);
                this.foundWordDictionary[word.Text] = go;
            }
        }
    }

    void UpdatePlayers(GameState gameState)
    {
        var playerFinds = new Dictionary<string, int[]>();

        foreach (var word in gameState.Words)
        {
            if (!playerFinds.ContainsKey(word.PlayerName))
            {
                playerFinds[word.PlayerName] = new int[2];
            }
            if (word.Valid)
            {
                playerFinds[word.PlayerName][0]++;
            }
            else
            {
                playerFinds[word.PlayerName][1]++;
            }
        }

       foreach (var player in playerFinds.Keys)
       {
            if (!this.playersDictionary.ContainsKey(player))
            {
                var go = Instantiate(NameStatusPrefab);
                go.transform.SetParent(this.Canvas.transform, false);
                this.playersDictionary[player] = go;
            }
            var obj = this.playersDictionary[player];
            var ns = obj.GetComponent<NameStatus>();
            ns.SetStatus(player, playerFinds[player][0]++,
                playerFinds[player][1]++);

        }
    }

    void ProcessGameState(GameState gameState)
    {
        TopScoreBoard.Update(gameState);
        UpdateWordsFound(gameState);

        if (this.levelIndex == -1)
        {
            this.levelIndex = gameState.LevelIndex;
        }

        if (gameState.LevelIndex != this.levelIndex)
        {
            NextBoard(gameState.LevelIndex);
        }
        BottomBarCanvas.UpdateState(gameState);

        UpdatePlayers(gameState);

        if (gameState.RemainingTime < 60 && !clockStarted)
        {
            clockStarted = true;
            Sounds.PlaySound(Sounds.clockAudioSource);
        }

        if (gameState.RemainingTime <= 0)
        {
            if (BottomBarCanvas.WordInputField.enabled)
            {
                Sounds.PlaySound(Sounds.GameOverSound);
            }
            BottomBarCanvas.WordInputField.enabled = false;
            BottomBarCanvas.WordInputField.text = "<game over>";

        }
    }

    void UpdateGame()
    {

        if (DateTime.Now.Ticks - this.lastGameUpdate >
            TimeSpan.TicksPerSecond)
        {
            this.lastGameUpdate = DateTime.Now.Ticks;
            Action<GameState> onGameState = gameState =>
            {
                ProcessGameState(gameState);
            };

            Action<string> onError = message => {
                Debug.Log(message);

            };
            var server = this.GetComponent<GamerServer>();
            StartCoroutine(server.GetGameState(this.game, onGameState, onError));
        }
    }
    // Update is called once per frame
    void Update()
    {
        if (this.game.Length > 0)
        {
            UpdateGame();
        }
    }
}
