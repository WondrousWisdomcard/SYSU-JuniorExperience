using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CCFlyAction : SSAction
{
    public float gravity;
    public float time;
    public Vector3 speed;
    public Vector3 force;

    public static CCFlyAction GetSSAction(DiskData diskData)
    {
        CCFlyAction action = ScriptableObject.CreateInstance<CCFlyAction>();
        action.gravity = 9.8f;
        action.time = 0;
        action.speed = diskData.speed;
        action.force = diskData.force;
        return action;
    }

    public override void Start()
    {
        this.gameObject.GetComponent<Rigidbody>().isKinematic = true;
    }

    public override void Update()
    {
        time += Time.deltaTime;
        transform.Translate(Vector3.down * gravity * time * Time.deltaTime 
            + speed * Time.deltaTime);

        if (this.transform.position.y < -10)
        {
            this.destroy = true;
            this.enable = false;
            this.callback.SSActionEvent(this);
        }
    }
}
