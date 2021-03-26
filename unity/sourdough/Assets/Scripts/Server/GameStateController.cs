using UnityEngine;
using System.Runtime.InteropServices;
public class GameStateController : MonoBehaviour
{
    [DllImport("__Internal")]
    public static extern void GameStarted();
}