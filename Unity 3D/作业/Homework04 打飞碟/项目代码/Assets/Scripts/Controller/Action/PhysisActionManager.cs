using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PhysisActionManager : SSActionManager, IActionManager, ISSActionCallback
{
    FirstController controller;
    PhysisFlyAction flyAction;

    protected new void Start(){
        controller = (FirstController)SSDirector.GetInstance().currentSceneController;
    }

    public void Fly(GameObject disk){
        flyAction = PhysisFlyAction.GetSSAction(disk.GetComponent<DiskData>());
        RunAction(disk, flyAction, this);
    }

    public void SSActionEvent(SSAction source,
        SSActionEventType events = SSActionEventType.Competed,
        int intParam = 0,
        string strParam = null,
        Object objectParam = null){

        controller.diskFactory.FreeDisk(source.gameObject);
    }
}
