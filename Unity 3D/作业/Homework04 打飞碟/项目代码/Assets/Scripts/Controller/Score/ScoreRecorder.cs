using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScoreRecorder : MonoBehaviour
{
    private int score = 0;

    public void UpdateScore(DiskData disk)
    {
        Debug.Log("Score +" + disk.score);
        score += disk.score;
    }
    
    public int GetScore(){
        return score;
    }

    public void Reset(){
        score = 0;
    }
}
