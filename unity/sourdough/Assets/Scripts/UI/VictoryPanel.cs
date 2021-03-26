using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

public class AwardInfo
{
    public string Tilte;
    public string Name;
    public Color Color;
    public string ImageName;
    public AwardInfo(string title, string name, Color color, string imageName)
    {
        this.Tilte = title;
        this.Name = name;
        this.Color = color;
        this.ImageName = imageName;
    }
}

public static class Helpers
{
    private static System.Random rng = new System.Random();

    public static void Shuffle<T>(this IList<T> list)
    {
        int n = list.Count;
        while (n > 1)
        {
            n--;
            int k = rng.Next(n + 1);
            T value = list[k];
            list[k] = list[n];
            list[n] = value;
        }
    }
}

public class VictoryPanel : MonoBehaviour
{
    public GameObject Awards;
    public Text FoundWordsText;
    public Text OtherValidWordsText;
    public Animator Animator;
    public GameObject AwardPrefab;

    // Use this for initialization
    void Start()
    {

    }
    private List<AwardInfo> GetAwardsOnePlayer(LastLevel level)
    {
        var player = level.Words[0].PlayerName;
        List<AwardInfo> awards = OnePlayerTimeAwards(level, player);
        OnePlayerCountBasedAwards(level, player, awards);

        return awards;
    }

    private static void OnePlayerCountBasedAwards(LastLevel level, string player, List<AwardInfo> awards)
    {
        int valid = 0;
        int invalid = 0;
        int longest = 0;
        int streak = 0;
        int longestStreak = 0;
        foreach (var w in level.Words)
        {
            if (w.Valid)
            {
                streak++;
                valid++;
            }
            else
            {
                streak = 0;
                invalid++;
            }
            longest = Mathf.Max(longest, w.Text.Length);
            longestStreak = Mathf.Max(longestStreak, streak);
        }
        if (longestStreak > 2)
        {
            awards.Add(new AwardInfo(string.Format("Streak - {0} ", longestStreak), player, new Color(.1f, .3f, .9f),
                "Images/ScienceTool_128_083"));
        }

        awards.Add(new AwardInfo(string.Format("Longest Word - {0}", longest), player, new Color(.2f, .2f, .7f),
            "Images/ScienceTool_128_062"));

        if (valid > 10)
        {
            awards.Add(new AwardInfo("Dime",
               player, new Color(.3f, .4f, .7f),
               "Images/ScienceTool_128_056"));
        }
        if (invalid > 10)
        {
            awards.Add(new AwardInfo("Brown Dime",
               player, new Color(.4f, .1f, .3f),
               "Images/ScienceTool_128_046"));
        }
    }

    private static List<AwardInfo> OnePlayerTimeAwards(LastLevel level, string player)
    {
        var awards = new List<AwardInfo>();
        if (level.EndTime - level.StartTime < 60)
        {
            awards.Add(new AwardInfo("Crazy Fast", player, new Color(.8f, .3f, 0),
                "Images/ScienceTool_128_085"));

        }
        else if (level.EndTime - level.StartTime < 120)
        {
            awards.Add(new AwardInfo("Super Fast", player, new Color(.7f, .2f, .3f),
                "Images/ScienceTool_128_086"));
        }

        return awards;
    }

    private static void MultiplayerAwards(LastLevel level, List<AwardInfo> awards, Dictionary<string, List<GameWord>> playerToWords)
    {
        MultiplayerTimeAwards(level, awards);

        MultiplayerLengthAwards(level, awards);

        MultiplayerWordAmountAwards(awards, playerToWords);

        MultiplayerFirstLastWordAwards(level, awards);
    }

    private static void MultiplayerFirstLastWordAwards(LastLevel level, List<AwardInfo> awards)
    {
        foreach (var w in level.Words)
        {
            if (w.Valid)
            {
                awards.Add(new AwardInfo("First Good Word",
                    level.Words[0].PlayerName,
                    new Color(.5f, .1f, .4f),
                    "Images/ScienceTool_128_024"));
                break;
            }

        }
        awards.Add(new AwardInfo("Last Good Word",
            level.Words[level.Words.Count - 1].PlayerName,
            new Color(.2f, .5f, .2f),
            "Images/ScienceTool_128_095"));
    }

    private static void MultiplayerWordAmountAwards(List<AwardInfo> awards, Dictionary<string, List<GameWord>> playerToWords)
    {
        int mostWords = 0;
        int leastWords = int.MaxValue;
        string mostName = "";
        string leastName = "";
        foreach (var playerName in playerToWords.Keys)
        {
            if (playerToWords[playerName].Count > 10)
            {
                awards.Add(new AwardInfo("Dime",
                    playerName, new Color(.3f, .4f, .7f),
                    "Images/ScienceTool_128_056"));
            }
            if (playerToWords[playerName].Count > mostWords)
            {
                mostName = playerName;
                mostWords = playerToWords[playerName].Count;
            }

            if (playerToWords[playerName].Count < leastWords)
            {
                leastName = playerName;
                leastWords = playerToWords[playerName].Count;
            }
        }
        awards.Add(new AwardInfo(string.Format("Most Found {0}", mostWords),
            mostName,
            new Color(.1f, .4f, .7f),
            "Images/ScienceTool_128_068"));
        awards.Add(new AwardInfo(string.Format("Least Found {0}", leastWords),
            leastName,
            new Color(.1f, .4f, .4f),
            "Images/ScienceTool_128_036"));
    }

    private static void MultiplayerLengthAwards(LastLevel level, List<AwardInfo> awards)
    {
        int longest = 0;
        string player = "";
        foreach (var w in level.Words)
        {
            if (longest < w.Text.Length)
            {
                longest = w.Text.Length;
                player = w.PlayerName;
            }
        }

        awards.Add(new AwardInfo(string.Format("Longest Word {0}",
                longest),
            player,
            new Color(.2f, .2f, .7f),
            "Images/ScienceTool_128_062"));
    }

    private static void MultiplayerTimeAwards(LastLevel level, List<AwardInfo> awards)
    {
        if (level.EndTime - level.StartTime < 60)
        {
            awards.Add(new AwardInfo("Crazy Fast", "All Yinz", new Color(.8f, .3f, 0),
                "Images/ScienceTool_128_085"));

        }
        else if (level.EndTime - level.StartTime < 120)
        {
            awards.Add(new AwardInfo("Super Fast", "All Yinz", new Color(.7f, .2f, .3f),
                "Images/ScienceTool_128_086"));
        }
        else if (level.EndTime - level.StartTime < 180)
        {
            awards.Add(new AwardInfo("Fast", "All Yinz", new Color(.7f, .4f, .3f),
                "Images/ScienceTool_128_087"));
        }
    }

    private List<AwardInfo> GetAwards(LastLevel level)
    {
        var awards = new List<AwardInfo>();
        //group words by users
        var playerToWords = new Dictionary<string,
            List<GameWord>>();
        foreach (var w in level.Words)
        {
            if (!playerToWords.ContainsKey(w.PlayerName))
            {
                playerToWords[w.PlayerName] = new List<GameWord>();
            }
            playerToWords[w.PlayerName].Add(w);
        }
        if (playerToWords.Count == 1)
        {
            return GetAwardsOnePlayer(level);
        }
        else
        {
            MultiplayerAwards(level, awards, playerToWords);

        }
        return awards;
    }

    public void ShowLevel(LastLevel level)
    {
        //remove old awards
        ClearAwards();

        var awards = GetAwards(level);
        awards = CleanUpAwards(awards);

        CreateAwards(awards);

        this.FoundWordsText.text = level.FoundWords;
        this.OtherValidWordsText.text = level.OtherValid;

        this.Show();
    }

    private void CreateAwards(List<AwardInfo> awards)
    {
        foreach (var awardInfo in awards)
        {
            var go = Instantiate(this.AwardPrefab);
            var award = go.GetComponent<Award>();
            award.SetAward(awardInfo.Tilte, awardInfo.Name, awardInfo.ImageName, awardInfo.Color);
            go.transform.SetParent(this.Awards.transform);
            go.transform.localScale = Vector3.one;
        }
    }

    private static List<AwardInfo> CleanUpAwards(List<AwardInfo> awards)
    {
        Helpers.Shuffle<AwardInfo>(awards);
        if (awards.Count > 6)
        {
            awards = awards.GetRange(0, 6);
        }

        return awards;
    }

    private void ClearAwards()
    {
        foreach (Transform child in Awards.transform)
        {
            Destroy(child.gameObject);
        }
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void Show()
    {
        this.Animator.Play("Zoom In");
    }

    public void Close()
    {
        this.Animator.Play("Zoom Out");
    }

}