using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ScoreBoard : MonoBehaviour
{
    public Text TimeText;
    public Text GoalText;
    public Text ValidWordsText;
    public Text InvalidWordsText;
    public Text LevelText;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Update(GameState state)
    {
        LevelText.text = "L" + state.LevelIndex.ToString();
        GoalText.text = state.RemainingWords.ToString();
        if (state.RemainingTime > 60)
        {
            TimeText.text = ((int)state.RemainingTime / 60).ToString() + "m";
        }
        else
        {
            TimeText.text = ((int)state.RemainingTime).ToString() + "s";
        }
        ValidWordsText.text = state.ValidWords.ToString();
        InvalidWordsText.text = state.InvalidWords.ToString();
    }
}
