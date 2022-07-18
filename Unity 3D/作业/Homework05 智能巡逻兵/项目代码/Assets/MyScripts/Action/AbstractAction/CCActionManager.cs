using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CCActionManager : SSActionManager, ISSActionCallback
{
    FirstController controller;

    protected new void Start(){
        controller = (FirstController)SSDirector.GetInstance().CurrentSceneController;
    }

    public void SSActionEvent(SSAction source,
        SSActionEventType events = SSActionEventType.Completed,
        int intParam = 0,
        string strParam = null,
        Object objectParam = null){
    }
}
