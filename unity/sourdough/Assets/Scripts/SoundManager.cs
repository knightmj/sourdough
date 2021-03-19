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
    public bool Mute = false;
    public SoundManager()
    {
    }

    public void PlaySound(AudioClip clip)
    {
        if (!this.Mute)
            Source.PlayOneShot(clip);
    }

}
