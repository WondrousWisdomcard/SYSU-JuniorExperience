
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CCMoveToAction: SSAction{
    public Vector3 target;
    public float speed;

    public static CCMoveToAction GetSSAction(Vector3 target, float speed){
        CCMoveToAction action = ScriptableObject.CreateInstance<CCMoveToAction>();
        action.target = target;
        action.speed = speed;
        return action;
    } 

    public override void Update(){
        if(this.destory == true){
            return;
        }
        this.transform.position = Vector3.MoveTowards(transform.position, target, speed);
        if(this.transform.position == this.target){
            this.destory = true;
            this.callback.SSActionEvent(this);
        }
    }

    public override void Start(){
    }
}

// 似曾相识的运动代码。动作完成，并发出事件通知，期望管理程序自动回收运行对象。