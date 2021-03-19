using System;
using System.Collections.Generic;

public class GameWord
{
    public string PlayerName;
    public string Text;
    public bool Valid;

    public GameWord(SimpleJSON.JSONNode node)
    {
        if (node["text"] != null)
        {
            Text = node["text"].Value; 
        }
        if (node["player"] != null)
        {
            PlayerName = node["player"].Value;
        }
        if (node["valid"] != null)
        {
            Valid = node["valid"].AsBool;
        }
    }
}
public class GameState
{
    public int LevelIndex;
    public List<string> PlayerNames = new List<string>();
    public float RemainingTime;
    public int RemainingWords;
    public int ValidWords;
    public int InvalidWords;
    public string RuleText;
    public List<GameWord> Words = new List<GameWord>();

    public GameState(string jsonText)
    {
        SimpleJSON.JSONNode gameState = SimpleJSON.JSON.Parse(jsonText);

        if (gameState["level_index"] != null)
        {
            LevelIndex = gameState["level_index"].AsInt;
        }
        if (gameState["remaining_words"] != null)
        {
            RemainingWords = gameState["remaining_words"].AsInt;
        }
        if (gameState["valid_words"] != null)
        {
            ValidWords = gameState["valid_words"].AsInt;
        }
        if (gameState["invalid_words"] != null)
        {
            InvalidWords = gameState["invalid_words"].AsInt;
        }
        if (gameState["remaining_time"] != null)
        {
            RemainingTime = gameState["remaining_time"].AsFloat;
        }
        if (gameState["rule_text"] != null)
        {
            RuleText = gameState["rule_text"].Value;
        }
        if (gameState["players"] != null)
        {
            foreach(var node in gameState["players"].AsArray)
            {
                PlayerNames.Add(node.Value);
            }
        }
        if (gameState["words"] != null)
        {
            foreach (var node in gameState["words"].AsArray)
            {
                Words.Add(new GameWord(node));
            }
        }
    }
}
