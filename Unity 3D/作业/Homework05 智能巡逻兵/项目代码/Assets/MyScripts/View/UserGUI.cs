using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UserGUI : MonoBehaviour
{
    IUserAction userAction;
    string scoreText;

    public bool gameover;
    public bool win;
    public bool start;

    void Start(){
        userAction = SSDirector.GetInstance().CurrentSceneController as IUserAction;
        gameover = false;
        win = false;
        start = false;
        scoreText = "Collect All Gems to Win | Score: 0 | Gem: 10 | Time: 0s";
    }
     
    public void UpdateScoreText(int score, int restGem, int second){
        scoreText = "Collect All Gems to Win | Score: " + score + " | RestGem: " + restGem + " | Time:" + second + "s";
    }

    void OnGUI(){

        if (Input.anyKeyDown) {
            start = true;
        }

        GUIStyle RestartStyle = new GUIStyle();
        RestartStyle.normal.background = Resources.Load<Texture2D>("Icon/Restart");

        GUIStyle ScoreTextStyle = new GUIStyle();
        ScoreTextStyle.normal.textColor = Color.white;
        ScoreTextStyle.fontSize = 20;
        ScoreTextStyle.alignment = TextAnchor.MiddleCenter;

        if(GUI.Button(new Rect(Screen.width - 50, 0, 50, 50), " ", RestartStyle)) {
            userAction.Restart();
            gameover = false;
            scoreText = "Collect All Gems to Win | Score: 0 | Gem: 10 | Time: 0s";
        }
        
        GUI.Button(new Rect(30, 10, Screen.width - 60, 50), scoreText, ScoreTextStyle);

        GUIStyle GameStartStyle = new GUIStyle();
        GameStartStyle.normal.textColor = Color.white;
        GameStartStyle.fontSize = 30;
        GameStartStyle.alignment = TextAnchor.MiddleCenter;
        if(gameover == true) {
            GUI.Button(new Rect(30, 30, Screen.width - 60, Screen.height - 60), "G A M E  O V E R", GameStartStyle);
        }
        else if(win == true) {
            GUI.Button(new Rect(30, 30, Screen.width - 60, Screen.height - 60), "G O O D  J O B", GameStartStyle);
        }
        else if(start == false) {
            GUI.Button(new Rect(30, 30, Screen.width - 60, Screen.height - 60), "S T A R T", GameStartStyle);
        }
    }
}
