using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterGUI : UserGUI
{
    private CharacterModel character;

    public void SetCharacterGUI(int clickedObjectType, CharacterModel character){
        this.clickedObjectType = clickedObjectType;
        if(clickedObjectType == CHARACTER){
            this.character = character;
        }
    }

    void OnMouseDown(){
        userAction.clickCharacter(character);
    }
}

