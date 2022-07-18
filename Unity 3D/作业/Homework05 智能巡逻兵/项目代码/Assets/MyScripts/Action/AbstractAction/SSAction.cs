using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SSAction : ScriptableObject
{
    public bool enable = true;
    public bool destroy = false;

    public GameObject gameObject { get; set; }
    public Transform transform { get; set; }
    public ISSActionCallback callback { get; set; }

    protected SSAction() {

    }

    // 初始化动作
    public virtual void Start() {
        throw new System.NotImplementedException();
    }

    // 每帧更新动作
    public virtual void Update() {
        throw new System.NotImplementedException();
    }

    public void Reset() {
        enable = false;
        destroy = false;
        gameObject = null;
        transform = null;
        callback = null;
    }
}