package info.gridworld.maze;

import info.gridworld.actor.*;
import info.gridworld.grid.*;

import java.awt.Color;
import java.util.ArrayList;
import java.util.Random;
import java.util.Stack;

import java.security.SecureRandom;
import javax.swing.JOptionPane;

/**
 * A <code>MazeBug</code> can find its way in a maze. <br />
 * The implementation of this class is testable on the AP CS A and AB exams.
 */
public class MazeBug extends Bug {

	// next: 下一个移动到的位置，在 move 方法中，Bug 会移动到 next 位置
	public Location next;

	// isEnd: 判断是否到达了终点，每次 canMove 会检查四周是否有出口（红石头）
	//        如果找到则将 isEnd 置为 true
	public boolean isEnd = false;

	/** crossLoaction: DFS核心栈结构，每一个栈单元是一个 Location 的链表
	 *				即 ArrayList<Location>
	 *
	 * 由于 DFS 需要标记或记录来实现路径回溯
	 * 我们在探索一个新的位置时，会打包一个"位置信息"入栈
	 * - 在前进时，我们查看栈顶的"位置信息"选择下一个移动位置
	 * - 若没有可移动的位置，回溯，我们弹出栈顶的"位置信息"，并返回上一个位置
	 *
	 * 一个 "位置信息" ArrayList<Location> 的内容定义如下：
	 * - ArrayList<Location>[0] : 保存的是该位置的上一个位置
	 * 				例如当前位置是(1,0)，从(0,0)移动而来
	 * 				则当前栈顶的ArrayList<Location>[0] 是 (0,0)
	 * - ArrayList<Location>[i] : i > 0 保存的是该位置下一步的还可以走的位置
	 *  			每当我们从栈顶选择一个向前走，就从栈顶删除该Location
	 * 				以此来实现一个标记的过程。
	 **/	
	public Stack<ArrayList<Location>> crossLocation = new 			Stack<ArrayList<Location>>();

	// stepCount: 计算总探索步数（包括回溯带来的花销）
	// pathLength：计算从起点到终点的最短路径长度（不含错误探索和回溯）
	public Integer stepCount = 0;
	public Integer pathLength = 0;

	// 以下是为启发式搜索提供的数据结构

	// FourMoves: 0 - NORTH; 1 - EAST; 2 - SOUTH; 3 - WEST; 
	// 统计正确路径上每个方向的步数
	private Integer[] fourMoves = new Integer[4];

	// State: 0 - GO AHEAD, 1 - GO BACK
	// 当前状态是 往前探索新路径 / 进行回溯
	public static int GO_AHEAD = 0;
	public static int GO_BACK = 1;
	private Integer state = GO_AHEAD;

	boolean hasShown = false;
	/**
	 * Constructs a box bug that traces a square of a given side length
	 */
	public MazeBug() {
		setColor(Color.GREEN);
		for(int i = 0; i < 4; i++){
			fourMoves[i] = 1;
		}
	}

	/**
	 * Print top of stack
	 */
	private void showStackTop(){
		ArrayList<Location> top = crossLocation.peek();
		for(Location l : top){
			System.out.print(l.toString() + " ");
		}
	}

	/**
	 * Strategy of select next step 
	 * @param level level-1 means select with optimizing strategy
	 */
	private void selectNext(int level){
		ArrayList<Location> record = crossLocation.peek();
		if(level == 1){
			boolean bools[] = new boolean[4];
			int times[] = new int[4];
			int positions[] = new int[4];
			int sum = 0;

			for(int i = 0; i < 4; i++){
				bools[i] = false;
				times[i] = 0;
			}

			for(int i = 1; i < record.size(); i++){
				int direction = getLocation().getDirectionToward(record.get(i));
				bools[direction / 90] = true;
				positions[direction / 90] = i;
			}

			for(int i = 0; i < 4; i++){
				if(bools[i]){
					times[i] = fourMoves[i];
					sum += times[i];
				}
			}
			if(sum <= 0){
				next = record.get(1);
				return;
			}
			
			SecureRandom random = new SecureRandom();
        		int ran = random.nextInt(sum);

			if(ran < times[0]){
				next = record.get(positions[0]);
			}
			else if(ran < times[0] + times[1]){
				next = record.get(positions[1]);
			}
			else if(ran < times[0] + times[1] + times[2]){
				next = record.get(positions[2]);
			}
			else{
				next = record.get(positions[3]);
			}
		}
		else{
			next = record.get(1);
		}
		
	}

	/**
	 * Moves to the next location of the square.
	 */
	public void act() {
	
		if(stepCount == 0){
			ArrayList<Location> firstRecord = new ArrayList<Location>();
			firstRecord.add(getLocation());
			for(Location loc : getValid(getLocation())){
				firstRecord.add(loc);
			}
			if(firstRecord.size() > 1){
				crossLocation.push(firstRecord);
			}
		}

		boolean willMove = canMove();

		if (isEnd == true) {
			// Case 1: 到达终点并显示步数
			if (hasShown == false) {
				String msg = stepCount.toString() + " steps";
				JOptionPane.showMessageDialog(null, msg);
				hasShown = true;
			}
		} else if (willMove) {
			// Case 2: 向前移动，更新步数
			state = GO_AHEAD;
			selectNext(1);
			ArrayList<Location> headRecord = crossLocation.pop();
			Location now = getLocation();			
			headRecord.remove(next);
			crossLocation.push(headRecord);
			move();
			stepCount++;
			pathLength++;

			ArrayList<Location> newRecord = new ArrayList<Location>();
			newRecord.add(now);
			for(Location loc : getValid(getLocation())){
				newRecord.add(loc);
			}
			crossLocation.push(newRecord);
			
		} else {
			// Case 3: 无路可走，回溯返回
			state = GO_BACK;			

			ArrayList<Location> headRecord = crossLocation.pop();
			next = headRecord.get(0);
			move();
			stepCount++;
			pathLength--;

		}
	}

	/**
	 * Find all positions that can be move to.
	 * 
	 * @param loc the location to detect.
	 * @return List of positions.
	 */
	public ArrayList<Location> getValid(Location loc) {
		Grid<Actor> gr = getGrid();
		if (gr == null)
			return null;
		ArrayList<Location> valid = new ArrayList<Location>();
		
		int[] dirs = {Location.AHEAD, Location.LEFT, Location.RIGHT};
		for(int dir : dirs){
			Location nextLoc = loc.getAdjacentLocation(getDirection() + dir);
            if (gr.isValid(nextLoc))
                valid.add(nextLoc);
		}

		if(stepCount == 0){
			Location backLoc = loc.getAdjacentLocation(getDirection() + Location.HALF_CIRCLE);
            if (gr.isValid(backLoc))
                valid.add(backLoc);
		}

		return valid;
	}

	/**
	 * Tests whether this bug can move forward into a location that is empty or
	 * contains a flower.
	 * 
	 * @return true if this bug can move.
	 */
	public boolean canMove() {
		Grid<Actor> gr = getGrid();
		boolean flag = false;
        if (gr == null)
            return false;

		ArrayList<Location> record = crossLocation.pop();
		for(int i = 1; i < record.size(); i++){
			Location nextLoc = record.get(i);
			Actor neighbor = gr.get(nextLoc);
			if((neighbor instanceof Rock) && neighbor.getColor().equals(Color.RED)){
				isEnd = true;
			}
			else if(neighbor == null || (neighbor instanceof Flower)){
				flag = true;
			}
			else{
				if(record.remove(nextLoc)){
					i--;
				}
			}
		}
		crossLocation.push(record);

		return flag;
	}

	/**
	 * Move to next, next is a location decided by the program
	 */
	public void move() {
		Grid<Actor> gr = getGrid();
		if (gr == null)
			return;
		Location loc = getLocation();
		if (gr.isValid(next)) {
			setDirection(getLocation().getDirectionToward(next));
			
			if(state == GO_AHEAD){
				fourMoves[getDirection() / 90]++;
			}
			else{
				fourMoves[getDirection() / 90]--;
				if(fourMoves[getDirection() / 90] <= 0){
					fourMoves[getDirection() / 90] = 0;
				}
			}

			moveTo(next);
		} else
			removeSelfFromGrid();
		Flower flower = new Flower(getColor());
		flower.putSelfInGrid(gr, loc);
	}

}
