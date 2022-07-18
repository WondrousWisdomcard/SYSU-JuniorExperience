using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterGUI : UserGUI
{
    private CharacterModel characterModel;

    public void SetCharacterGUI(int clickedObjectType, CharacterModel characterModel){
        this.clickedObjectType = clickedObjectType;
        if(clickedObjectType == CHARACTER){
            this.characterModel = characterModel;
        }
    }

    void OnMouseDown(){
        userAction.clickCharacter(characterModel);
    }
}

