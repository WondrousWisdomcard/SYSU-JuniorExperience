using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public enum SSActionEventType : int {Completed, Started};
public interface ISSActionCallback{
    void SSActionEvent(
        SSAction source, 
        SSActionEventType events = SSActionEventType.Completed, 
        int intParam = 0, 
        string strParam = null, 
        Object objectParam = null);
}