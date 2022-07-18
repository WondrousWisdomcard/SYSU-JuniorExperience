using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Robot
{
    private int[,] priorityMatrix = new int[3,3]; // The position with the highest priority is what robot chooses 

    public Robot(){
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                priorityMatrix[i, j] = 0;
            }
        }
    }

    // Return the position [x,y], which is the decision of robots
    public int[] decisionMaking(ChessBoard chessboard, Player robot, Player player, int turns){
        int [,] chessMatrix = chessboard.getChessMatrix();
        int [] XY = new int[2];
        if(robot.isFirstHand() && turns == 0){
            XY = getRandomXY();
        }
        else{
            int robotChessStyle = robot.getChessStyle();
            int playerChessStyle = player.getChessStyle();

            XY = decisionMakingII(chessMatrix, robotChessStyle, playerChessStyle);
        }
        return XY;
    }

    private int[] getRandomXY(){
        int[] XY = new int[2];
        XY[0] = Random.Range(0, 3);
        XY[1] = Random.Range(0, 3);
        return XY;
    }


    private int[] decisionMakingII(int[,] chessMatrix, int robotChessStyle, int playerChessStyle){

        int[,] weightMatrix = new int[3,3];

        int[] lineWeight = new int[8];

        const int level0 = 0;
        const int level1 = -50;
        const int level2 = 60;

        // Compute the weight matrix
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                if(chessMatrix[i, j] == robotChessStyle){
                    weightMatrix[i, j] = level2;
                }
                else if(chessMatrix[i, j] == playerChessStyle){
                    weightMatrix[i, j] = level1;
                }
                else{
                    weightMatrix[i, j] = level0;
                }
            }
        }

        // Compute line weight vector(8-dim)
        /*
              0          1          2
            X X X      . . .      . . .
            . . .  OR  X X X  OR  . . .
            . . .      . . .      X X X
        */
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                lineWeight[i] += weightMatrix[i, j];
            }
        }
        /*
              3          4          5
            X . .      . X .      . . X
            X . .  OR  . X .  OR  . . X
            X . .      . X .      . . X
        */
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                lineWeight[i + 3] += weightMatrix[j, i];
            }
        }
        /*
              6
            X . .   
            . X .  
            . . X 
        */
        lineWeight[6] = weightMatrix[0, 0] + weightMatrix[1, 1] + weightMatrix[2, 2];
        /*
              7
            . . X   
            . X .  
            X . . 
        */
        lineWeight[7] = weightMatrix[0, 2] + weightMatrix[1, 1] + weightMatrix[2, 0];


        // Compute the priority matrix
        priorityMatrix[0, 0] = System.Math.Max(System.Math.Max(System.Math.Abs(lineWeight[0]), System.Math.Abs(lineWeight[3])), System.Math.Abs(lineWeight[6]));
        priorityMatrix[0, 1] = System.Math.Max(System.Math.Abs(lineWeight[0]),System.Math.Abs(lineWeight[4]));
        priorityMatrix[0, 2] = System.Math.Max(System.Math.Max(System.Math.Abs(lineWeight[0]), System.Math.Abs(lineWeight[5])), System.Math.Abs(lineWeight[7]));

        priorityMatrix[1, 0] = System.Math.Max(System.Math.Abs(lineWeight[1]),System.Math.Abs(lineWeight[3]));
        priorityMatrix[1, 1] = System.Math.Max(System.Math.Max(System.Math.Max(System.Math.Abs(lineWeight[1]), System.Math.Abs(lineWeight[4])), System.Math.Abs(lineWeight[6])), System.Math.Abs(lineWeight[7]));
        priorityMatrix[1, 2] = System.Math.Max(System.Math.Abs(lineWeight[1]),System.Math.Abs(lineWeight[5]));

        priorityMatrix[2, 0] = System.Math.Max(System.Math.Max(System.Math.Abs(lineWeight[2]), System.Math.Abs(lineWeight[3])), System.Math.Abs(lineWeight[7]));
        priorityMatrix[2, 1] = System.Math.Max(System.Math.Abs(lineWeight[2]),System.Math.Abs(lineWeight[4]));
        priorityMatrix[2, 2] = System.Math.Max(System.Math.Max(System.Math.Abs(lineWeight[2]), System.Math.Abs(lineWeight[3])), System.Math.Abs(lineWeight[6]));

        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                if(chessMatrix[i, j] == robotChessStyle){
                    priorityMatrix[i, j] = 0;
                }
                else if(chessMatrix[i, j] == playerChessStyle){
                    priorityMatrix[i, j] = 0;
                }
            }
        }

        // Choose the position with the highest priority
        int max = 0, x = 0, y = 0;
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                
                int isEq = Random.Range(0, 2);
                if(isEq == 0){
                    if(priorityMatrix[i, j] > max){
                        max = priorityMatrix[i, j];
                        x = i;
                        y = j;
                    }
                }
                else{
                    if(priorityMatrix[i, j] >= max){
                        max = priorityMatrix[i, j];
                        x = i;
                        y = j;
                    }
                }
            }
        }
        
        int [] XY = new int[2];
        XY[0] = x;
        XY[1] = y;
        return XY;
    }

    // For testing
    public string printPriorityMatrix(){
        string info = "ThePriorityMatrix\n";
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 3; j++){
                info += priorityMatrix[i, j].ToString() + " ";
            }
            info += "\n";
        }
        return info;
    }
}
