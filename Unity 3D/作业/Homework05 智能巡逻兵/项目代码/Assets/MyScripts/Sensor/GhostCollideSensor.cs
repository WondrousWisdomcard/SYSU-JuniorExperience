using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 幽灵碰撞检测器：用于检测玩家是否与幽灵发生了接触
public class GhostCollideSensor : MonoBehaviour
{
    FirstController sceneController;
    void OnTriggerEnter(Collider collider) {
        sceneController = SSDirector.GetInstance().CurrentSceneController as FirstController;
        if (collider.gameObject.Equals(sceneController.player)) {
            // 幽灵抓到玩家
            Debug.Log("Ghost: Catch U!");
            Singleton<GameEventManager>.Instance.OnPlayerCatched();
        }
        else {
            // 幽灵碰到障碍物
            Debug.Log("Ghost: Oops!");
            this.GetComponent<GhostData>().isCollided = true;
        }
    }
}