using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player
{
    private int winCount; // Total winning times
    private int chessStyle; // 0-O 1-X
    private bool firstHand; // 是否为先手

    public Player(int chessStyle, bool firstHand){
        this.winCount = 0;
        this.chessStyle = chessStyle;
        this.firstHand = firstHand;
    }
    
    public void setWinCount(){
        winCount++;
    }

    public int getWinCount(){
        return winCount;
    }

    public void resetWinCount(){
        winCount = 0;
    }

    public void setChessStyle(int i){
        chessStyle = i;
    }

    public int getChessStyle(){
        return chessStyle;
    }

    public void changeFirstHand(){
        firstHand = !firstHand;
    }

    public bool isFirstHand(){
        return firstHand;
    }
}
