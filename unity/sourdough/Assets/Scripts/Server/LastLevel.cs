using System;
using System.Collections.Generic;

public class LastLevel
{
    public List<GameWord> Words = new List<GameWord>();
    public float StartTime;
    public float EndTime;
    List<string> Valid = new List<string>();
    public LastLevel(string jsonText)
    {
        SimpleJSON.JSONNode lastLevel = SimpleJSON.JSON.Parse(jsonText);
        if (lastLevel["start_time"] != null)
        {
            this.StartTime = lastLevel["start_time"].AsFloat;
        }
        if (lastLevel["end_time"] != null)
        {
            this.EndTime = lastLevel["end_time"].AsFloat;
        }
        if (lastLevel["level"] != null)
        {
            if (lastLevel["level"]["valid"] != null)
            {
                foreach (var v in lastLevel["level"]["valid"].AsArray)
                {
                    this.Valid.Add(v.Value);
                }
            }
        }
        if (lastLevel["words"] != null)
        {
            foreach (var node in lastLevel["words"].AsArray)
            {
                Words.Add(new GameWord(node));
            }
        }
    }

    public string FoundWords
    {
        get
        {
            string text = "";
            foreach(var w in this.Words)
            {
                if (w.Valid)
                    text += w.Text + " ";
            }
            return text;
        }
    }
    public string OtherValid
    {
        get
        {
            HashSet<string> foundWords = new HashSet<string>();
            foreach (var w in this.Words)
            {
                if (w.Valid)
                    foundWords.Add(w.Text);
            }
            string text = "";
            foreach (var w in this.Valid)
            {
                if (!foundWords.Contains(w))
                    text += w + " ";
            }
            return text;
        }
    }
}
