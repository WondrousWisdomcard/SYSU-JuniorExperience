using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 宝石碰撞检测器：被挂载在宝石上，用于检测玩家是否接触到宝石
public class GemCollideSensor : MonoBehaviour
{
    FirstController sceneController;      // 当前的场记
    void OnTriggerEnter(Collider collider) {
        sceneController = SSDirector.GetInstance().CurrentSceneController as FirstController;
        if (collider.gameObject.Equals(sceneController.player)) {
            // 玩家获取宝石
            Singleton<GameEventManager>.Instance.GettingGem(this.gameObject);
        }
    }
}