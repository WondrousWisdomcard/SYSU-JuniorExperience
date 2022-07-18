using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SSActionManager : MonoBehaviour
{

    private Dictionary<int, SSAction> actions = new Dictionary<int, SSAction>();

    // 待执行动作队列和待删除动作队列
    private List<SSAction> waitingAdd = new List<SSAction>();
    private List<int> waitingDelete = new List<int>();

    // 执行待执行动作，执行结束后删除
    protected void Update()
    {
        foreach (SSAction action in waitingAdd)
        {
            actions[action.GetInstanceID()] = action;
        }
        waitingAdd.Clear();
        foreach (KeyValuePair<int, SSAction> kv in actions)
        {
            SSAction action = kv.Value;
            if (action.enable)
            {
                action.Update();
            }
            else if (action.destroy)
            {
                waitingDelete.Add(action.GetInstanceID()); // release action
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

    // 添加待执行动作
    public void RunSSAction(GameObject gameObject, SSAction action, ISSActionCallback callback)
    {
        action.gameObject = gameObject;
        action.transform = gameObject.transform;
        action.callback = callback;
        waitingAdd.Add(action);
        action.Start();
    }

    // 标记销毁所有动作
    public void DestroyAll()
    {
        foreach (KeyValuePair<int, SSAction> kv in actions)
        {
            SSAction ac = kv.Value;
            ac.destroy = true;
        }
    }

    protected void Start() {
        // Do Nothing
    }
}
