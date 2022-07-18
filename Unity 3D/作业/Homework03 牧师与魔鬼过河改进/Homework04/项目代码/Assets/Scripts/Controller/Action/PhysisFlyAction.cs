using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PhysisFlyAction : SSAction
{
    float gravity;
    float time;
    Vector3 speed;
    Vector3 force;

    public static PhysisFlyAction GetSSAction(DiskData diskData)
    {
        PhysisFlyAction action = ScriptableObject.CreateInstance<PhysisFlyAction>();
        action.gravity = 9.8f;
        action.time = 0;
        action.speed = diskData.speed;
        action.force = diskData.force;
        return action;
    }

    public override void Start()
    {
        this.gameObject.GetComponent<Rigidbody>().isKinematic = false;
        this.gameObject.GetComponent<Rigidbody>().velocity = speed;
        this.gameObject.GetComponent<ConstantForce>().force = force;
        this.gameObject.GetComponent<ConstantForce>().torque = new Vector3(0.2F, 0, -0.2F);
    }

    public override void Update()
    {
        if (this.transform.position.y < -10)
        {
            this.destroy = true;
            this.enable = false;
            this.callback.SSActionEvent(this);
        }
    }
}
