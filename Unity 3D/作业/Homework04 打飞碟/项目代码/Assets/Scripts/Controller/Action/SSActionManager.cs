using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SSActionManager : MonoBehaviour
{
    private Dictionary<int, SSAction> actions = new Dictionary<int, SSAction>();

    private List<SSAction> waitingAdd = new List<SSAction>();
    private List<int> waitingDelete = new List<int>();

    protected void Update()
    {
        foreach (SSAction ac in waitingAdd){
            actions[ac.GetInstanceID()] = ac;
        }
        waitingAdd.Clear();

        foreach (KeyValuePair<int, SSAction> pair in actions){
            SSAction action = pair.Value;
            if (action.destroy)
            {
                waitingDelete.Add(action.GetInstanceID());
            }
            else if (action.enable)
            {
                action.Update();
            }
        }

        foreach (int key in waitingDelete)
        {
            SSAction action = actions[key];
            actions.Remove(key);
            Destroy(action);
        }
        waitingDelete.Clear();
    }

    public void RunAction(GameObject gameObject, SSAction action, ISSActionCallback manager)
    {
        action.gameObject = gameObject;
        action.transform = gameObject.transform;
        action.callback = manager;
        waitingAdd.Add(action);
        action.Start();
    }

    protected void Start()
    {
    }

}