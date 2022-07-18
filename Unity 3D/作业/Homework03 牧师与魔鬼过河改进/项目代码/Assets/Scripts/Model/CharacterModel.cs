using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterModel{
    private GameObject character;
    private CharacterGUI characterGUI;
    private Vector3 initialPosition;

    private int characterType;
    private int characterState;

    public static int PRIEST = 0;
    public static int DEVIL = 1; 
    public static int ASHORE_START = 0;
    public static int ASHORE_DESTINATION = 1;
    public static int ONBOARD = 2;

    public CharacterModel(int characterType, string characterName, Vector3 position){
        this.characterType = characterType;
        this.characterState = ASHORE_START;
        this.initialPosition = position;

        if(characterType == PRIEST){
            character = Object.Instantiate (Resources.Load ("Prefabs/Priest", typeof(GameObject)), Vector3.zero, Quaternion.identity, null) as GameObject;
        }
        else if(characterType == DEVIL){
            character = Object.Instantiate (Resources.Load ("Prefabs/Devil", typeof(GameObject)), Vector3.zero, Quaternion.identity, null) as GameObject;
        }

        character.name = characterName;  
        character.transform.position = position;
        characterGUI = character.AddComponent (typeof(CharacterGUI)) as CharacterGUI;
        characterGUI.SetCharacterGUI(UserGUI.CHARACTER, this);
    }

    public int getCharacterType(){
        return characterType;
    }

    public int getCharacterState(){
        return characterState;
    }

    public Vector3 getInitialPosition(){
        return initialPosition;
    }

    public GameObject getGameObject(){
        return character;
    }

    public void setCharacterState(int characterState){
        this.characterState = characterState;
    }

    public void setCharacterPosition(Vector3 position){
        character.transform.position = position;
    }

    public void resetCharacter(){
        characterState = ASHORE_START;
        setCharacterPosition(initialPosition);
    }
}