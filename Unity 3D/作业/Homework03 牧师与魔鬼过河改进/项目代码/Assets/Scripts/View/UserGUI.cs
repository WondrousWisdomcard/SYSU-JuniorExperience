using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class UserGUI: MonoBehaviour{
    protected IUserAction userAction;
    protected int clickedObjectType;
    public static int CHARACTER = 0;
    public static int BOAT = 1;

    void Start(){
        userAction = Director.getInstance().currentSceneController as IUserAction;
    }

}