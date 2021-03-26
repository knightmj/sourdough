using System;
using UnityEngine;

public class SoundManager : MonoBehaviour
{
    //public Audio
    public AudioClip validWordAudioSource;
    public AudioClip invalidWordAudioSource;
    public AudioClip knownWordAudioSource;
    public AudioClip levelUpAudioSource;
    public AudioClip clockAudioSource;
    public AudioClip GameOverSound;
    public AudioSource Source;
    public SoundManager()
    {
    }

    public void PlaySound(AudioClip clip)
    {
        if (!this.Mute)
            Source.PlayOneShot(clip);
    }
    public bool Mute
    {
        get { return Source.mute; }
        set { Source.mute = value;}
    }
}
