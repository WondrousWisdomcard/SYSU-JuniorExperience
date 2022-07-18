using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 计分器：每幽摆脱一个幽灵的追击，获得 1 分
public class ScoreRecorder : MonoBehaviour
{
    public int score;

    void Start() {
        score = 0;
    }

    public void Record(int i) {
        score += i;
    }

    public void Reset() {
        score = 0;
    }
}