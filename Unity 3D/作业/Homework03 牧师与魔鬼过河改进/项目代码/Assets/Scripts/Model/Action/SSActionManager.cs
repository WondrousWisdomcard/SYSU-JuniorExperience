using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SSActionManager : MonoBehaviour{
    private Dictionary <int, SSAction> actions = new Dictionary<int, SSAction>();
    private List<SSAction> waitingAdd = new List<SSAction>();
    private List<int> waitingRemove = new List<int>();

    protected bool unlock = true;

    protected void Update(){
        foreach (SSAction action in waitingAdd){
            actions[action.GetInstanceID()] = action;
        }
        waitingAdd.Clear();

        foreach (KeyValuePair<int, SSAction> pair in actions){
            SSAction action = pair.Value;
            if(action.destory){
                waitingRemove.Add(action.GetInstanceID());
            }
            else if(action.enable){
                action.Update();
            }
        }

        foreach (int key in waitingRemove){
            SSAction action = actions[key];
            actions.Remove(key);
            Destroy(action);
        }
        waitingRemove.Clear();
    }

    public void RunAction(GameObject gameObject, SSAction action, ISSActionCallback manager){
        action.gameObject = gameObject;
        action.transform = gameObject.transform;
        action.callback = manager;
        waitingAdd.Add(action);
        action.Start();
    }

    public bool getUnlock(){
        return unlock;
    }

    protected void Start(){
        Debug.Log("SSAction Manager Start");
    }
}