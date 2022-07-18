using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChessBoard
{
    private int [,] ChessMatrix = new int[3,3];
    private bool [,] WinChessMatrix = new bool[3,3]; // WinChessMatrix is set to highlight the Chessboard

    private const int O = 0, X = 1, Empty = -1;

    public void cleanChessMatrix(){
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                ChessMatrix[i,j] = Empty;
                WinChessMatrix[i,j] = false;
            }
        }
    }    

    // Update the chess matrix with position [i,j]
    public bool updateChessMatrix(int player, int  i, int j){
        if(ChessMatrix[i, j] == Empty){
            ChessMatrix[i, j] = player;
            return true;
        }
        else{
            return false;
        }
    }

    public int [,] getChessMatrix(){
        return ChessMatrix;
    }

    public bool [,] getWinChessMatrix(){
        return WinChessMatrix;
    }

    public int whoWin(){

        /* Situation 1:
        X X X    X . .
        . . . or X . .
        . . .    X . .
        */
        for(int i = 0; i < 3; i++){
            if(ChessMatrix[0,i] == ChessMatrix[1,i] && ChessMatrix[1,i] == ChessMatrix[2,i]){
                if(ChessMatrix[0,i] == O){
                    WinChessMatrix[0,i] = WinChessMatrix[1,i] = WinChessMatrix[2,i] = true;
                    return O;
                }
                else if(ChessMatrix[0,i] == X){
                    WinChessMatrix[0,i] = WinChessMatrix[1,i] = WinChessMatrix[2,i] = true;
                    return X;
                }
            }
            
            if(ChessMatrix[i,0] == ChessMatrix[i,1] && ChessMatrix[i,1] == ChessMatrix[i,2]){
                if(ChessMatrix[i,0] == O){
                    WinChessMatrix[i,0] = WinChessMatrix[i,1] = WinChessMatrix[i,2] = true;
                    return O;
                }
                else if(ChessMatrix[i,0] == X){
                    WinChessMatrix[i,0] = WinChessMatrix[i,1] = WinChessMatrix[i,2] = true;
                    return X;
                }
            }

        }

        /* Situation 2:
        X . .    . . X
        . X . or . X .
        . . X    X . .
        */
        if(ChessMatrix[0,0] == ChessMatrix[1,1] && ChessMatrix[1,1] == ChessMatrix[2,2]){
            if(ChessMatrix[0,0] == O){
                WinChessMatrix[0,0] = WinChessMatrix[1,1] = WinChessMatrix[2,2] = true;
                return O;
            }
            else if(ChessMatrix[0,0] == X){
                WinChessMatrix[0,0] = WinChessMatrix[1,1] = WinChessMatrix[2,2] = true;
                return X;
            }
        }
        else if(ChessMatrix[2,0] == ChessMatrix[1,1] && ChessMatrix[1,1] == ChessMatrix[0,2]){
            if(ChessMatrix[2,0] == O){
                WinChessMatrix[2,0] = WinChessMatrix[1,1] = WinChessMatrix[0,2] = true;
                return O;
            }
            else if(ChessMatrix[2,0] == X){
                WinChessMatrix[2,0] = WinChessMatrix[1,1] = WinChessMatrix[0,2] = true;
                return X;
            }
        }

        return Empty;
    }
}
