using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SceneGUI : MonoBehaviour
{
    private IUserAction userAction;
    private bool unlock;
    private int gameState;

    public static int UNKNOWN = 0;
    public static int WIN = 1;
    public static int LOSE = 2;

    void Start(){
        unlock = true;
        gameState = 0;
        userAction = Director.getInstance().currentSceneController as IUserAction;
    }

    public void setGameState(int state){
        gameState = state;
    }

    public bool getUnlock(){
        return unlock;
    }

    void OnGUI(){
        GUI.skin = Resources.Load <GUISkin> ("Skin/MySkin");

        // Restart Button
        if(GUI.Button(new Rect(Screen.width - 50, 0, 50, 50), " ")) {
            setGameState(UNKNOWN);
            userAction.gameRestart();
            unlock = true;
        }

        if(gameState == WIN){
            unlock = false;
            GUI.Label(new Rect(Screen.width / 2 - 200, Screen.height / 2 - 100, 400, 200), Resources.Load <Texture2D> ("Skin/Win"));
        }
        else if(gameState == LOSE){
            unlock = false;
            GUI.Label(new Rect(Screen.width / 2 - 200, Screen.height / 2 - 100, 400, 200), Resources.Load <Texture2D> ("Skin/Gameover"));
            
        }
    }
}
