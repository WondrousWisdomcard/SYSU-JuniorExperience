using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// 摄像头控制器：需要手动挂载到主摄像机上
public class CameraController : MonoBehaviour
{
	public GameObject player;
    public float distanceAway = 3F;		 	// 摄像头离玩家的水平距离	
	public float distanceUp = 3F;			// 摄像头离地面的垂直距离		
	public float smooth = 2F;				// 平滑变换参数
		
	private Vector3 m_TargetPosition;		// 摄像头的位置
	
	Transform follow;        				// 摄像头望向的位置
	
	void Start(){
		
	}
	
	void LateUpdate ()
	{
		follow = player.transform.GetChild(2);
		
		// 设置摄像头的目标位置
		m_TargetPosition = follow.position + Vector3.up * distanceUp - follow.forward * distanceAway;
		
		// 对移动过程进行平滑变换
		transform.position = Vector3.Lerp(transform.position, m_TargetPosition, Time.deltaTime * smooth);
		
		// 望向指定位置
		transform.LookAt(follow);
	}
}

