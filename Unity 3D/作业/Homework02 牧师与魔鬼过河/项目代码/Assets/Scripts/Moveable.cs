using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Moveable: MonoBehaviour{

    public static int WAITING = 0;
    public static int EMBARK = 1;
    public static int SHIPING = 2;
    public static int DISEMBARK = 3;

    private const float SPEED = 0.1F;
    private Vector3 destPosition;
    private int currentState;

    public void Update(){
        if(currentState != WAITING && transform.position != destPosition){
            transform.position = Vector3.MoveTowards(transform.position, destPosition, SPEED);
        }
        else{
            currentState = WAITING;
        }

        // if(currentState == EMBARK){            
        // }
        // else if(currentState == SHIPING){
        // }
        // else if(currentState == DISEMBARK){
        // }
        // else if(currentState == WAITING){
        // }
    }


    public void setDestPosition(Vector3 destPosition){
        this.destPosition = destPosition;
    }

    public void setCurrentState(int currentState){
        this.currentState = currentState;
    }

    public int getCurrentState(){
        return this.currentState;
    }
    
    public void resetMoveable(){
        currentState = WAITING;
    }
}