using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoatGUI : UserGUI
{
    private BoatModel boatModel;

    public void SetBoatGUI(int clickedObjectType, BoatModel boatModel){
        this.clickedObjectType = clickedObjectType;
        if(clickedObjectType == BOAT){
            this.boatModel = boatModel;
        }
    }

    void OnMouseDown(){
        userAction.clickBoat(boatModel);    
    }
}
