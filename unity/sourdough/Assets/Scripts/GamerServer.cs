using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class GamerServer: MonoBehaviour
{
    static string server = "http://sourdoughwordgames.com";
    public IEnumerator LoadBoard(string game, Action<string[][]> boardLoaded,  Action<string> error)
    {
        var request = UnityWebRequest.Get(server + "/get_board?game=" + game);

        yield return request.SendWebRequest();

        if (request.isNetworkError || request.isHttpError)
        {
            error(request.error);
        }
        else
        {
            // Show results as text
            var boardJson = SimpleJSON.JSON.Parse(request.downloadHandler.text);
            var newLetters = new string[boardJson.AsArray.Count][];

            int rowIndex = 0;
            foreach (SimpleJSON.JSONNode row in boardJson)
            {
                newLetters[rowIndex] = new string[row.AsArray.Count];
                int letterIndex = 0;
                foreach (var letter in row.AsArray)
                {
                    newLetters[rowIndex][letterIndex++] = letter.Value;
                }
                rowIndex++;
            }
            boardLoaded(newLetters);     
        }
    }
    public IEnumerator GetGameState(string game,
       Action<GameState> gameState, Action<string> error)
    {
        string url = String.Format("{0}/get_game_data?game={1}",
            server,
            game);

        var request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();
        if (request.isNetworkError || request.isHttpError)
        {
            error(request.error);
        }
        else
        {

            gameState(new GameState(request.downloadHandler.text));
        }
    }
    public IEnumerator AddWord(string game, string word, string player,
        Action<bool,bool, string> wordAdded, Action<string> error)
    {
        string url = String.Format("{0}/add_word?game={1}&word={2}&player={3}",
            server,
            game,
            word,
            player);

        var request = UnityWebRequest.Get(url);

        yield return request.SendWebRequest();

        if (request.isNetworkError || request.isHttpError)
        {
            error(request.error);
        }
        else
        {
            SimpleJSON.JSONNode wordResult = SimpleJSON.JSON.Parse(request.downloadHandler.text);
            if (wordResult["valid"] != null)
            {
                if (wordResult["valid"].AsBool)
                {
                    wordAdded(false, true, "word matched");
                }
                else
                {
                    wordAdded(false, false, "word didn't follow rule");
                }
            }
            else
            {
                wordAdded(true, false, wordResult["invalid"].Value);
            }
        }
    }
}
