using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainSceneController : MonoBehaviour, ISceneController, IUserAction
{
    
    Vector3 riverPosition = new Vector3(0,0,0); // 10 X 10 X 1
    Vector3 leftBankPosition = new Vector3(-35,0,0); // 10 X 10 X 1.2
    Vector3 rightBankPosition = new Vector3(35,0,0); // 10 X 10 X 1.2
    Vector3 boatStartPosition = new Vector3(5,0,0); // 2 X 4 X 0.5
    Vector3 boatDestinationPosition = new Vector3(-5,0,0); 
    Vector3[] characterInitPosition = new Vector3[6];

    public GameObject river, leftBank, rightBank;
    public BoatModel boat;
    public CharacterModel[] priests = new CharacterModel[3];
    public CharacterModel[] devils = new CharacterModel[3];

    public SceneGUI sceneGUI;
    public CCActionManager actionManager;
    public Referee referee;

    void Awake(){
        Debug.Log("Preparing...");
        Director director = Director.getInstance();
        director.currentSceneController = this;
        director.currentSceneController.loadResources();
        sceneGUI = gameObject.AddComponent (typeof(SceneGUI)) as SceneGUI;
        actionManager = gameObject.AddComponent (typeof(CCActionManager)) as CCActionManager;
        referee = new Referee();
    }

    void generateGameObjects(){
        // River
        river = Instantiate <GameObject> (Resources.Load <GameObject> ("Prefabs/River"), riverPosition, Quaternion.identity);
        river.name = "River";

        // The Bank
        // leftBank = Instantiate <GameObject> (Resources.Load <GameObject> ("Prefabs/RiverBank"), leftBankPosition, Quaternion.identity);
		// leftBank.name = "DestBank";
        // rightBank = Instantiate <GameObject> (Resources.Load <GameObject> ("Prefabs/RiverBank"), rightBankPosition, Quaternion.identity);
		// rightBank.name = "StartBank";
        
        // Boat
        boat = new BoatModel(boatStartPosition, boatDestinationPosition);

        // Priests & Devils
        for(int i = 0; i < 6; i++){
            characterInitPosition[i] = rightBankPosition + new Vector3(-25F, 0, i * 1.5F - 3.75F);
        }

        priests[0] = new CharacterModel(CharacterModel.PRIEST, "Justica", characterInitPosition[0]);
        priests[1] = new CharacterModel(CharacterModel.PRIEST, "Kindmes", characterInitPosition[1]);
        priests[2] = new CharacterModel(CharacterModel.PRIEST, "Loyalti", characterInitPosition[2]);

        devils[0] = new CharacterModel(CharacterModel.DEVIL, "Gred", characterInitPosition[3]);
        devils[1] = new CharacterModel(CharacterModel.DEVIL, "Arroganca", characterInitPosition[4]);
        devils[2] = new CharacterModel(CharacterModel.DEVIL, "Lazi", characterInitPosition[5]);
    }

    public void loadResources(){
        Debug.Log("Loading resources...");
        generateGameObjects();
    }

    public void gameRestart(){
        Debug.Log("Restart game...");
        boat.resetBoat();
        for(int i = 0; i < 3; i++){
            priests[i].resetCharacter();
            devils[i].resetCharacter();
        }
    }

    public void clickCharacter(CharacterModel character){
        if(character.getCharacterType() == CharacterModel.PRIEST){
            Debug.Log("Priest clicked");
        }
        else if(character.getCharacterType() == CharacterModel.DEVIL){
            Debug.Log("Devil clicked");
        }

        int RightToLeft = 1;
        int LeftToRight = -1;

        if(character.getCharacterState() == CharacterModel.ASHORE_START && boat.getBoatState() == BoatModel.PARKING_START){
            // StartBank 上船
            if(boat.getEmptySitsCount() != 0){
                actionManager.goOnShipAction(character.getGameObject(), boat.getASit(character), LeftToRight);
                character.setCharacterState(CharacterModel.ONBOARD);
            } 
        }
        else if(character.getCharacterState() == CharacterModel.ASHORE_DESTINATION && boat.getBoatState() == BoatModel.PARKING_DESTINATION){
            // DestinationBank 上船
            if(boat.getEmptySitsCount() != 0){
                actionManager.goOnShipAction(character.getGameObject(), boat.getASit(character), RightToLeft);
                character.setCharacterState(CharacterModel.ONBOARD);
            }
        }
        else if(character.getCharacterState() == CharacterModel.ONBOARD){
            if(boat.getBoatState() == BoatModel.PARKING_START){ 
                // StartBank 下船
                boat.leaveASit(character);
                actionManager.goOffShipAction(character.getGameObject(), character.getInitialPosition(), LeftToRight);
                character.setCharacterState(CharacterModel.ASHORE_START);

            }
            else if(boat.getBoatState() == BoatModel.PARKING_DESTINATION){
                // DestinationBank 下船
                boat.leaveASit(character);
                Vector3 destination = character.getInitialPosition() - Vector3.right * 2 * character.getInitialPosition().x;
                actionManager.goOffShipAction(character.getGameObject(), destination, RightToLeft);
                character.setCharacterState(CharacterModel.ASHORE_DESTINATION);
            }
        }

    }

    public void clickBoat(BoatModel boat){
        Debug.Log("Boat clicked");
        if(boat.getOccupiedSitsCount() != 0){
            if(boat.getBoatState() == BoatModel.PARKING_START){
                // StartBank -> DestinationBank
                boat.setBoatState(BoatModel.SHIPING);
                actionManager.shipingAction(boat.getGameObject(), boat.getDestinationPosition());
                boat.setBoatState(BoatModel.PARKING_DESTINATION);
            }
            else if(boat.getBoatState() == BoatModel.PARKING_DESTINATION){
                // DestinationBank -> StartBank
                boat.setBoatState(BoatModel.SHIPING);
                actionManager.shipingAction(boat.getGameObject(), boat.getStartPosition());
                boat.setBoatState(BoatModel.PARKING_START);
            }
        }
    }

    void Update(){
        if(sceneGUI.getUnlock() == true && actionManager.getUnlock() == true){
            if(referee.gameJudge() == -1){
                sceneGUI.setGameState(SceneGUI.LOSE);
            }
            else if(referee.gameJudge() == 1){
                sceneGUI.setGameState(SceneGUI.WIN);
            }
        }
    }
}
