using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoatGUI : UserGUI
{
    private BoatModel boat;

    public void SetBoatGUI(int clickedObjectType, BoatModel boat){
        this.clickedObjectType = clickedObjectType;
        if(clickedObjectType == BOAT){
            this.boat = boat;
        }
    }

    void OnMouseDown(){
        userAction.clickBoat(boat);    
    }
}
