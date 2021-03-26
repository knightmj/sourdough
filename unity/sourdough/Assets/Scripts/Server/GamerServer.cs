using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class GamerServer : MonoBehaviour
{
	public string Host = "http://0.0.0.0:80";
	public IEnumerator LoadBoard(string game, Action<string[][]> boardLoaded, Action<string> error)
	{
		var request = UnityWebRequest.Get(Host + "/get_board?game=" + game);

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

	public IEnumerator GetGameState(string game, Action<GameState> gameState, Action<string> error)
	{
		string url = String.Format("{0}/get_game_data?game={1}", Host, game);

		var request = UnityWebRequest.Get(url);
		yield
		return request.SendWebRequest();
		if (request.isNetworkError || request.isHttpError)
		{
			error(request.error);
		}
		else
		{

			gameState(new GameState(request.downloadHandler.text));
		}
	}

	public IEnumerator AddWord(string game, string word, string player, Action<bool, bool, string> wordAdded, Action<string> error)
	{
		string url = String.Format("{0}/add_word?game={1}&word={2}&player={3}", Host, game, word, player);

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

	public IEnumerator GetDeadLetters(string game, Action<string[]> deadLetters, Action<string> error)
	{
		string url = String.Format("{0}/dead_letters?game={1}", Host, game);

		var request = UnityWebRequest.Get(url);
		yield return request.SendWebRequest();
		if (request.isNetworkError || request.isHttpError)
		{
			error(request.error);
		}
		else
		{
			var lettersJson = SimpleJSON.JSON.Parse(request.downloadHandler.text);
			var letters = new string[lettersJson.AsArray.Count];
			for (int i = 0; i < lettersJson.AsArray.Count; i++)
			{
				letters[i] = lettersJson.AsArray[i];

			}
			deadLetters(letters);
		}
	}

	public IEnumerator GetLastlevel(string game, Action<LastLevel> lastLevel, Action<string> error)
	{
		string url = String.Format("{0}/get_last_level?game={1}", Host, game);
		var request = UnityWebRequest.Get(url);
		yield return request.SendWebRequest();

		if (request.isNetworkError || request.isHttpError)
		{
			error(request.error);
		}
		else
		{
			lastLevel(new LastLevel(request.downloadHandler.text));
		}

	}
}