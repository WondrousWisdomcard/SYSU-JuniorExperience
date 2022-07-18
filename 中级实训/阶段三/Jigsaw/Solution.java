package solution;

import java.util.*;

import jigsaw.Jigsaw;
import jigsaw.JigsawNode;


/**
 * 在此类中填充算法，完成重拼图游戏（N-数码问题）
 */
public class Solution extends Jigsaw {

    private List<JigsawNode> solutionPath;  // 解路径：用以保存从起始状态到达目标状态的移动路径中的每一个状态节点
    private int searchedNodesNum;           // 已访问节点数：用以记录所有访问过的节点的数量

    private LinkedList<JigsawNode> openList;  // 用以保存已发现但未访问的节点
    private LinkedList<JigsawNode> colseList;    // 用以保存已发现的节点

    /**
     * 拼图构造函数
     */
    public Solution() {
    }

    /**
     * 拼图构造函数
     * @param bNode - 初始状态节点
     * @param eNode - 目标状态节点
     */
    public Solution(JigsawNode bNode, JigsawNode eNode) {
        super(bNode, eNode);
    }

    /**
     *（实验一）广度优先搜索算法，求指定5*5拼图（24-数码问题）的最优解
     * 填充此函数，可在Solution类中添加其他函数，属性
     * @param bNode - 初始状态节点
     * @param eNode - 目标状态节点
     * @return 搜索成功时为true,失败为false
     */
    public boolean BFSearch(JigsawNode bNode, JigsawNode eNode) {

        colseList = new LinkedList<JigsawNode>();
        openList = new LinkedList<JigsawNode>();

        beginJNode = new JigsawNode(bNode);
        endJNode = new JigsawNode(eNode);
        currentJNode = null;
        searchedNodesNum = 0;
        solutionPath = null;

        final int DIRS = 4;

        // (1)将起始节点放入openList中
        openList.add(beginJNode);

        // (2) 如果openList为空，或者访问节点数大于MAX_NODE_NUM个，则搜索失败，问题无解；否则循环直到求解成功
        while (!openList.isEmpty()) {
        
        	searchedNodesNum++;
        	
            // (2-1)取出openList的第一个节点N，置为当前节点currentJNode
            //      若currentJNode为目标节点，则搜索成功，计算解路径，退出
            currentJNode = openList.peek();
            if (currentJNode.equals(eNode)) {
                getPath();
                break;
            }

            // (2-2)从openList列表中删除节点v，放入colseList列表中
            openList.remove(currentJNode);
            colseList.add(currentJNode);

            // 记录并显示搜索过程
            // System.out.println("Searching.....Number of searched nodes:" + searchedNodesNum +
            //     "    Est:" + currentJNode.getEstimatedValue() +
            //     "    Current state:" + currentJNode.toString());

            JigsawNode[] nextNodes = new JigsawNode[]{
                new JigsawNode(currentJNode), new JigsawNode(currentJNode),
                new JigsawNode(currentJNode), new JigsawNode(currentJNode)
            };

            // (2-3)寻找所有与currentJNode邻接且未曾被发现的节点，将它们插入openList中
            for (int i = 0; i < DIRS; i++) {
                if (nextNodes[i].move(i) && !colseList.contains(nextNodes[i])) {
                    openList.add(nextNodes[i]);
                }
            }
        }

        System.out.println("Jigsaw AStar Search Result:");
        System.out.println("Begin state:" + getBeginJNode().toString());
        System.out.println("End state:" + getEndJNode().toString());
        System.out.println("Total number of searched nodes:" + searchedNodesNum);
        System.out.println("Depth of the current node is:" + getCurrentJNode().getNodeDepth());
        
        return isCompleted();
    }


    /**
     *（Demo+实验二）计算并修改状态节点jNode的代价估计值:f(n)
     * 如 f(n) = s(n). s(n)代表后续节点不正确的数码个数
     * 此函数会改变该节点的estimatedValue属性值
     * 修改此函数，可在Solution类中添加其他函数，属性
     * @param jNode - 要计算代价估计值的节点
     */
         
    public void estimateValue(JigsawNode jNode) {
        // s: 估价函数是
        int s = 0; 
        int dimension = JigsawNode.getDimension();
        for (int index = 1; index < dimension * dimension; index++) {
            if (jNode.getNodesState()[index] + 1 != jNode.getNodesState()[index + 1]) {
                s++;
            }
        }
        
        int[] nodeState = jNode.getNodesState();
        int[] endState = endJNode.getNodesState();

        // manhattan: 估价函数是两个状态的曼哈顿距离，
        //            即各个数码移动到目的位置的距离的总和
        // euclid:    
        // reverse:   估价函数是每一对逆转数码乘以一个倍数
        // error:     
        
        int manhattan = 0;
        int euclid = 0;
        int reverse = 0;
        int error = 0;

        for(int i = 1; i < dimension * dimension + 1; i++) {
        
        	if(nodeState[i] != endState[i]){
            	error += 1;
            }
                
            for(int j = 1; j < dimension * dimension + 1; j++) {
                if(nodeState[i] == endState[j] && nodeState[i] != 0) {
                	int dx = i / dimension - j / dimension;
                	int dy = i % dimension - j % dimension;
                    manhattan += Math.abs(dx);
                    manhattan += Math.abs(dy);
                    
                    euclid += Math.sqrt(dx * dx + dy * dy);
                }

                if(nodeState[i] == endState[j] && nodeState[j] == endState[i] && i != j) {
                    reverse += 1;
                }
               
            }
        }
        
        int sum = manhattan * 11 + error * 4 +  + s * 30 + reverse * 0 + euclid * 0;
        	
        jNode.setEstimatedValue(sum);
    }
}
