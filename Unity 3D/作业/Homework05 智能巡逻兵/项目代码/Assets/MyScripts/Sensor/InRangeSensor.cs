using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 幽灵范围感知器：挂载在幽灵的第一个子对象上（一个可穿透的半径为 5 的不可见球）
// 用于检测玩家是否位于幽灵的感知范围内
public class InRangeSensor : MonoBehaviour
{
    FirstController sceneController;
    public GameObject ghost;

    void OnTriggerEnter(Collider collider) {
        sceneController = SSDirector.GetInstance().CurrentSceneController as FirstController;
        if (collider.gameObject.Equals(sceneController.player)) {
            ghost.GetComponent<GhostData>().isInRange = true;
        }
    }
    void OnTriggerExit(Collider collider) {
        sceneController = SSDirector.GetInstance().CurrentSceneController as FirstController;
        if (collider.gameObject.Equals(sceneController.player)) {
            // 玩家离开幽灵视线
            ghost.GetComponent<GhostData>().isInRange = false;
        }
    }
}
