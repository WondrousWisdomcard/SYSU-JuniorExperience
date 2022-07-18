using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;

public class TheGame : MonoBehaviour
{
    // Texture2D Object
    public GUISkin customSkin;
    public GUIStyle whiteBackground;
    public Texture2D restartLogo;
    public Texture2D singleModeLogo, doubleModeLogo;
    public Texture2D O, X, Empty;
    public Texture2D O_Light, X_Light;

    // Layout Constant
    private const int gamePadHeight = 400;
    private const int gamePadWidth = 600;
    private const int chessSideLength = 100;
    private const int padding = 50;

    // Game Mode
    private const int SINGLE = 1, DOUBLE = 2;

    // ChessBoard and Players
    private ChessBoard chessboard;
    private Player player1, player2;
    private Robot robot;


    private int gameMode;
    private int turns; // Game Turns: 0-8
    private int dogfall; // Count of Dogfall
    private bool unlock; // The chessboard is lock when someone win the game or the game is in dogfall

    void Start()
    {
        chessboard = new ChessBoard();
        chessboard.cleanChessMatrix();

        player1 = new Player(0, true);
        player2 = new Player(1, false);
        robot = new Robot();
        
        gameMode = SINGLE;
        turns = 0;
        dogfall = 0;
        unlock = true;
    }

    void OnGUI()
    {
        GUI.skin = customSkin;
         
        // Generate GamePad
        GUI.Box(new Rect(0, 0, Screen.width, Screen.height), ""); // Full Screen Game Pad
       
        GUI.BeginGroup(new Rect(Screen.width * 0.5f - 300, Screen.height * 0.5f - 200, gamePadWidth, gamePadHeight));

            GUI.Box(new Rect(padding + 2, padding + 2, 3 * chessSideLength - 4, 3 * chessSideLength - 4), "", whiteBackground); // 棋盘

            robotAction(); // 机器人回合：机器人下棋

            chessBoardUpdate(); // 显示棋子 + 玩家回合：玩家下棋

            gameCheck(); // 判定胜负
    
            GUI.Label(new Rect (2 * padding + 3 * chessSideLength, padding, 150, 100), "The Game"); // 游戏Title
            
            gradeLabelUpdate(); // 更新比分表
            
            GUI.BeginGroup(new Rect(2 * padding + 3 * chessSideLength, padding + 200, 150, 100));

                setResetButton(); // Reset Button: 重新开启一盘棋

                setGameModeButton(); // Game Mode Button: 更改游戏模式 - 人机/双人
            
            GUI.EndGroup ();

        GUI.EndGroup ();
    }
    
    private void setGameModeButton(){
        if(gameMode == SINGLE){
            if(GUI.Button(new Rect (100,30,40,40), singleModeLogo)){
                resetChessboard();
                gameMode = DOUBLE;
                player1.resetWinCount();
                player2.resetWinCount();
                dogfall = 0;
            }
        }
        else{
            if(GUI.Button(new Rect (100,30,40,40), doubleModeLogo)){
                resetChessboard();
                gameMode = SINGLE;
                player1.resetWinCount();
                player2.resetWinCount();
                dogfall = 0;
            }
        }
    }

    private void setResetButton(){
        if(GUI.Button(new Rect (10,30,40,40), restartLogo)){
            resetChessboard();
        }
    }

    private void gradeLabelUpdate(){
        string wininfo = player1.getWinCount().ToString() + " : " + dogfall.ToString() + " : " + player2.getWinCount().ToString();
        GUI.Label(new Rect (2 * padding + 3 * chessSideLength, padding + 100, 150, 100), wininfo);
    }

    private void chessBoardUpdate(){
        int [,] chessMatrix = chessboard.getChessMatrix();
        bool [,] winMatrix = chessboard.getWinChessMatrix();
        int chessStyleThisTurn = getChessStyleThisTurn();

        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                Texture2D texture;
                Texture2D texture_Light;

                if(chessMatrix[i, j] == player1.getChessStyle()){
                    texture = O;
                    texture_Light = O_Light;
                }
                else if(chessMatrix[i, j] == player2.getChessStyle()){
                    texture = X;
                    texture_Light = X_Light;
                }
                else{
                    texture = Empty;
                    texture_Light = Empty;
                }

                if(unlock == false && winMatrix[i,j] == false){
                    // Light Chesses for highlighting the winner
                    GUI.Button(new Rect(padding + j * chessSideLength + 2, padding + i * chessSideLength + 2, chessSideLength - 4, chessSideLength - 4), texture_Light);
                }
                else{ 
                    // OnClick
                    if(GUI.Button(new Rect(padding + j * chessSideLength + 2, padding + i * chessSideLength + 2, chessSideLength - 4, chessSideLength - 4), texture) && unlock){
                        if(gameMode == DOUBLE || gameMode == SINGLE && chessStyleThisTurn == player1.getChessStyle()){
                            if(chessboard.updateChessMatrix(chessStyleThisTurn, i, j)){
                                turns++;
                            }
                        }   
                    }
                }
            }
        }
    }

    private void resetChessboard(){
        turns = 0;
        unlock = true;
        chessboard.cleanChessMatrix();
        player1.changeFirstHand();
        player2.changeFirstHand();
    }

    private void robotAction(){
        int chessStyleThisTurn = getChessStyleThisTurn();
        if(unlock && gameMode == SINGLE && chessStyleThisTurn == player2.getChessStyle()){
            // Thread.Sleep(300);
            int [] XY = robot.decisionMaking(chessboard, player2, player1, turns);
            chessboard.updateChessMatrix(chessStyleThisTurn, XY[0], XY[1]);
            turns++;
            print(robot.printPriorityMatrix());
        }
                        
    }
    
    private int getChessStyleThisTurn(){
        int chessStyle;
        if(player1.isFirstHand()){
            chessStyle = (turns) % 2;
        }
        else{
            chessStyle = (turns + 1) % 2;
        }
        return chessStyle;
    }
    
    private void gameCheck(){
        if(unlock){
            int result = chessboard.whoWin();
            unlock = false;
            if(result == player1.getChessStyle()){
                player1.setWinCount();
            }
            else if(result == player2.getChessStyle()){
                player2.setWinCount();
            }
            else{
                if(turns == 9){
                    dogfall++;
                }
                else{
                    unlock = true;
                }
            }
        }
        
    }
}
