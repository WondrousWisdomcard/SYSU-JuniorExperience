using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UserGUI : MonoBehaviour
{
    IUserAction userAction;
    string scoreText;
    bool start, gameover;

    void Start(){
        userAction = SSDirector.GetInstance().currentSceneController as IUserAction;
        start = false;
        gameover = false;
        scoreText = "Round 1    Score: 0";
    }

    public void UpdateScoreText(int round, int score){
        if(round <= 5){
            scoreText = "Round " + round + "    Score: " + score;
        }
        else{
            scoreText = "Total Score: " + score;
            gameover = true;
        }
        
    }

    void OnGUI(){
        if(start == false){
            GUIStyle GameStartStyle = new GUIStyle();
            GameStartStyle.normal.textColor = Color.white;
            GameStartStyle.fontSize = 30;
            GameStartStyle.alignment = TextAnchor.MiddleCenter;

            if(GUI.Button(new Rect(30, 30, Screen.width - 60, Screen.height - 60), "CLICK TO START", GameStartStyle)) {
                userAction.GameStart();
                start = true;
                gameover = false;
            }
        }
        else{
            GUIStyle RestartStyle = new GUIStyle();
            RestartStyle.normal.background = Resources.Load<Texture2D>("Icon/Restart");

            GUIStyle ScoreTextStyle = new GUIStyle();
            ScoreTextStyle.normal.textColor = Color.white;
            ScoreTextStyle.fontSize = 20;
            ScoreTextStyle.alignment = TextAnchor.MiddleCenter;

            if(GUI.Button(new Rect(Screen.width - 50, 0, 50, 50), " ", RestartStyle)) {
                userAction.Restart();
                start = false;
                gameover = false;
            }

            GUI.Button(new Rect(30, 10, Screen.width - 60, 50), scoreText, ScoreTextStyle);

            if (Input.GetButtonDown("Fire1")){
                userAction.Hit(Input.mousePosition);
            }
        }

        if(gameover == true && start == true){
            GUIStyle GameStartStyle = new GUIStyle();
            GameStartStyle.normal.textColor = Color.white;
            GameStartStyle.fontSize = 30;
            GameStartStyle.alignment = TextAnchor.MiddleCenter;

            GUI.Button(new Rect(30, 30, Screen.width - 60, Screen.height - 60), "G A M E  O V E R", GameStartStyle);
        }
    }

    public void Reset(){
        start = false;
        gameover = false;
        scoreText = "Round 1    Score: 0";
    }
}
