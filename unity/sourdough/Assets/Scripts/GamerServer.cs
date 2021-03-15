using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class GamerServer: MonoBehaviour
{
    static string server = "http://0.0.0.0/";
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
            Debug.Log(request.downloadHandler.text);
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
    public IEnumerator AddBoard(string game, string word,
        Action<bool, string> wordAdded, Action<string> error)
    {
        string url = String.Format("{0}/add_word?game={1}&word={2}",
            server,
            game,
            word);

        var request = UnityWebRequest.Get(url);

        yield return request.SendWebRequest();

        if (request.isNetworkError || request.isHttpError)
        {
            error(request.error);
        }
        else
        {
            SimpleJSON.JSONNode wordResult = SimpleJSON.JSON.Parse(
                request.downloadHandler.text);
            if (wordResult["valid"] != null)
            {
                wordAdded(true,"");
            }
            else
            {
                wordAdded(false, wordResult["invalid"].Value);
            }
        }
    }
}
