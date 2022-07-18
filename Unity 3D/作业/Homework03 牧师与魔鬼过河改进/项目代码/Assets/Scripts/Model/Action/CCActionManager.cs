using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CCActionManager: SSActionManager, ISSActionCallback{
    public MainSceneController sceneController;

    public CCMoveToAction shiping;
    public CCSequenceAction goOnShip, goOffShip;

    protected new void Start(){
        sceneController = (MainSceneController)Director.getInstance().currentSceneController;
        sceneController.actionManager = this;
        shiping = CCMoveToAction.GetSSAction(Vector3.zero, 0.05F);
    }

    protected new void Update(){
        base.Update();
    }

    public void SSActionEvent(SSAction source, SSActionEventType events = SSActionEventType.Completed, int intParam = 0, string strParam = null, Object objectParam = null){
        unlock = true; // 移动完成后解锁
        if(source == shiping){
            Debug.Log("Shiping Finish");
        }
    }


    /*
    Direction: RightToLeft = 1 / LeftToRight = -1
    */
    public void goOnShipAction(GameObject gameobject, Vector3 destination, int direction){
        unlock = false; // 移动前先上锁
        CCMoveToAction move1 = CCMoveToAction.GetSSAction(gameobject.transform.position + new Vector3(2,0,0) * direction, 0.05F);
        CCMoveToAction move2 = CCMoveToAction.GetSSAction(new Vector3(gameobject.transform.position.x + 2 * direction, 0, 0), 0.05F);
        CCMoveToAction move3 = CCMoveToAction.GetSSAction(destination, 0.05F);
        goOnShip = CCSequenceAction.GetSSAction(0, 0, new List<SSAction> {move1, move2, move3});
        RunAction(gameobject, goOnShip, this);
    }

    /*
    Direction: RightToLeft = 1 / LeftToRight = -1
    */
    public void goOffShipAction(GameObject gameobject, Vector3 destination, int direction){
        unlock = false; // 移动前先上锁
        CCMoveToAction move1 = CCMoveToAction.GetSSAction(new Vector3(destination.x + 2 * direction, 0, 0), 0.05F);
        CCMoveToAction move2 = CCMoveToAction.GetSSAction(new Vector3(destination.x + 2 * direction, 0, destination.z), 0.05F);
        CCMoveToAction move3 = CCMoveToAction.GetSSAction(destination, 0.05F);
        goOffShip = CCSequenceAction.GetSSAction(0, 0, new List<SSAction> {move1, move2, move3});
        RunAction(gameobject, goOffShip, this);
    }

    
    public void shipingAction(GameObject gameobject, Vector3 destination){
        unlock = false; // 移动前先上锁
        shiping = CCMoveToAction.GetSSAction(destination, 0.05F);
        RunAction(gameobject, shiping, this);
    }
}