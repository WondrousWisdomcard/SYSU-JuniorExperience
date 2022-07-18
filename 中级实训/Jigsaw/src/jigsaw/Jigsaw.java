package jigsaw;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

import java.util.function.Predicate;

import java.util.Comparator;
import java.util.Queue;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.HashSet;
import java.util.List;
import java.util.ArrayList;


/**
 * 重拼图游戏（N-数码问题）
 * @author abe
 *
 */
public abstract class Jigsaw {
    protected JigsawNode beginJNode;        // 拼图的起始状态节点
    protected JigsawNode endJNode;          // 拼图的目标状态节点
    protected JigsawNode currentJNode;      // 拼图的当前状态节点

    private List<JigsawNode> solutionPath;  // 解路径：用以保存从起始状态到达目标状态的移动路径中的每一个状态节点
    private int searchedNodesNum;           // 已访问节点数：用以记录所有访问过的节点的数量

    private Queue<JigsawNode> exploreList;  // 用以保存已发现但未访问的节点
    private Set<JigsawNode> visitedList;    // 用以保存已发现的节点

    /**
     * 拼图构造函数
     */
    public Jigsaw() {
        this.beginJNode = null;
        this.endJNode = null;
        this.currentJNode = null;
        this.solutionPath = null;
        this.exploreList = null;
        this.visitedList = null;
        this.searchedNodesNum = 0;
    }

    /**
     * 拼图构造函数
     * @param bNode - 初始状态节点
     * @param eNode - 目标状态节点
     */
    public Jigsaw(JigsawNode bNode, JigsawNode eNode) {
        this.beginJNode = new JigsawNode(bNode);
        this.endJNode = new JigsawNode(eNode);
        this.currentJNode = new JigsawNode(bNode);
        this.solutionPath = null;
        this.exploreList = null;
        this.visitedList = null;
        this.searchedNodesNum = 0;
    }

    /**
     * 此函数用于打散拼图：将输入的初始状态节点jNode随机移动len步，返回其打散后的状态节点
     * @param jNode - 初始状态节点
     * @param len - 随机移动的步数
     * @return 打散后的状态节点
     */
    public static final JigsawNode scatter(JigsawNode jNode, int len) {
        int randomDirection;
        len += (int) (Math.random() * 2);
        JigsawNode jigsawNode = new JigsawNode(jNode);
        for (int t = 0; t < len; t++) {
            int[] movable = jigsawNode.canMove();
            do {
                randomDirection = (int) (Math.random() * 4);
            } while (0 == movable[randomDirection]);
            jigsawNode.move(randomDirection);
        }
        jigsawNode.setInitial();
        return jigsawNode;
    }

    /**
     * Returns true if the path with initial state and target state is valid.
     * @param path - a path which record every step from the initial state to the target state
     * @param startNode - a jigsaw node which indicate initial state
     * @param destNode - a jigsaw node which indicate target state
     * @return true if the path is valid
     */
    public static final boolean isValidPath(List<JigsawNode> path, JigsawNode startNode, JigsawNode destNode) {
        if (path == null || path.isEmpty() || path.contains(null)) {
            return false;
        }

        int len = path.size();
        if (!path.get(0).equals(destNode) ||
            !path.get(len - 1).equals(startNode)) {
            return false;
        }

        JigsawNode jNode = new JigsawNode(path.get(0));
        for (int i = 1; i < len; i++) {
            JigsawNode prev = path.get(i);
            if (!prev.isValid()) {
                return false;
            }
            int direction = prev.getNodesState()[0] - jNode.getNodesState()[0];
            if (direction == -1) {
                if (!jNode.moveEmptyLeft() || !jNode.equals(prev)) {
                    return false;
                }
            } else if (direction == 1) {
                if (!jNode.moveEmptyRight() || !jNode.equals(prev)) {
                    return false;
                }
            } else if (direction < 0) {
                if (!jNode.moveEmptyUp() || !jNode.equals(prev)) {
                    return false;
                }
            } else if (direction > 0) {
                if (!jNode.moveEmptyDown() || !jNode.equals(prev)) {
                    return false;
                }
            } else {
                return false;
            }
        }
        return true;
    }

    /**
     * 获取拼图的当前状态节点
     * @return currentJNode -  拼图的当前状态节点
     */
    public final JigsawNode getCurrentJNode() {
        return currentJNode;
    }

    /**
     * 设置拼图的初始状态节点
     * @param jNode - 拼图的初始状态节点
     */
    public final void setBeginJNode(JigsawNode jNode) {
        beginJNode = jNode;
    }

    /**
     * 获取拼图的初始状态节点
     * @return beginJNode - 拼图的初始状态节点
     */
    public final JigsawNode getBeginJNode() {
        return beginJNode;
    }

    /**
     * 设置拼图的目标状态节点
     * @param jNode - 拼图的目标状态节点
     */
    public final void setEndJNode(JigsawNode jNode) {
        this.endJNode = jNode;
    }

    /**
     * 获取拼图的目标状态节点
     * @return endJNode - 拼图的目标状态节点
     */
    public final JigsawNode getEndJNode() {
        return endJNode;
    }

    /**
     * 获取拼图的求解状态
     * @return isCompleted - 拼图已解为true；拼图未解为false
     */
    public final boolean isCompleted() {
        return this.solutionPath != null;
    }

    /**
     * 重置拼图的求解状态
     */
    public final void reset() {
        this.solutionPath = null;
    }

    /**
     * 获取解路径文本
     * @return 解路径solutionPath的字符串，若有解，则分行记录从初始状态到达目标状态的移动路径中的每一个状态节点；
     * 若未解或无解，则返回提示信息。
     */
    public final String getSolutionPath() {
        String str = new String();
        str += "Begin->";
        if (isCompleted()) {
            for (int i = solutionPath.size() - 1; i >= 0; i--) {
                str += solutionPath.get(i).toString() + "->";
            }
            str += "End";
        } else {
            str = "Jigsaw Not Completed.";
        }
        return str;
    }

    /**
     * Get the solution path.
     * @return solution path
     */
    public final List<JigsawNode> getPath() {
        if (this.solutionPath == null && this.currentJNode != null) {
            this.solutionPath = new ArrayList<JigsawNode>(this.currentJNode.getNodeDepth() + 1);
            JigsawNode jNode = this.currentJNode;
            while (jNode != null) {
                solutionPath.add(jNode);
                jNode = jNode.getParent();
            }
        }
        return this.solutionPath;
    }

    /**
     * 获取访问过的节点数searchedNodesNum
     * @return 返回所有已访问过的节点总数
     */
    public final int getSearchedNodesNum() {
        return searchedNodesNum;
    }

    /**
     * 将搜索结果写入文件中，同时显示在控制台
     * 若搜索失败，则提示问题无解，输出已访问节点数；
     * 若搜索成功，则输出初始状态beginJnode，目标状态endJNode，已访问节点数searchedNodesNum，路径深度nodeDepth和解路径solutionPath。
     * @param pw - 文件输出PrintWriter类对象，如果pw为null，则写入到D://Result.txt
     * @throws IOException
     */
    public final void printResult(PrintWriter pw) throws IOException{
        boolean flag = false;
        if (pw == null) {
            pw = new PrintWriter(new FileWriter("Result.txt"));// 将搜索过程写入D://BFSearchDialog.txt
            flag = true;
        }
        if (this.isCompleted() == true) {
            // 写入文件
            pw.println("Jigsaw Completed");
            pw.println("Begin state:" + this.getBeginJNode().toString());
            pw.println("End state:" + this.getEndJNode().toString());
            pw.println("Solution Path: ");
            pw.println(this.getSolutionPath());
            pw.println("Total number of searched nodes:" + this.getSearchedNodesNum());
            pw.println("Length of the solution path is:" + this.getCurrentJNode().getNodeDepth());


            // 输出到控制台
            System.out.println("Jigsaw Completed");
            System.out.println("Begin state:" + this.getBeginJNode().toString());
            System.out.println("End state:" + this.getEndJNode().toString());
            System.out.println("Solution Path: ");
            System.out.println(this.getSolutionPath());
            System.out.println("Total number of searched nodes:" + this.getSearchedNodesNum());
            System.out.println("Length of the solution path is:" + this.getCurrentJNode().getNodeDepth());


        } else {
            // 写入文件
            pw.println("No solution. Jigsaw Not Completed");
            pw.println("Begin state:" + this.getBeginJNode().toString());
            pw.println("End state:" + this.getEndJNode().toString());
            pw.println("Total number of searched nodes:"
                    + this.getSearchedNodesNum());

            // 输出到控制台
            System.out.println("No solution. Jigsaw Not Completed");
            System.out.println("Begin state:" + this.getBeginJNode().toString());
            System.out.println("End state:" + this.getEndJNode().toString());
            System.out.println("Total number of searched nodes:"
                    + this.getSearchedNodesNum());
        }
        if (flag) {
            pw.close();
        }
    }


    /**
     * Removes all of the elements.
     */
    public final void prune() {
        this.exploreList.clear();
    }

    /**
     * Removes all of the elements of {@code exploreList} that satisfy the given predicate.
     * @param filter - a predicate which returns true for elements to be removed
     * @return true if any elements were removed
     */
    public final boolean prune(Predicate<JigsawNode> filter) {
        return this.exploreList.removeIf(i -> filter.test(new JigsawNode(i)));
    }



    // ****************************************************************
    // *************************实验任务*******************************
    /**
     * 实验任务一：广度优先搜索算法，求指定5*5拼图（24-数码问题）的最优解
     * 要求：完成广度优先搜索算法BFSearch()
     * 主要涉及函数：BFSearch()
     */
    /**
     * 实验任务二：启发式搜索算法，求解随机5*5拼图（24-数码问题）
     * 要求：1.完成代价估计函数estimateValue()
     *      2.访问节点总数不超过29000个
     * 主要涉及函数：ASearch()，estimateValue()
     */
    // ****************************************************************

    /**
     *（实验一）广度优先搜索算法，求指定5*5拼图（24-数码问题）的最优解。
     * @param bNode - 初始状态节点
     * @param eNode - 目标状态节点
     * @return 搜索成功时为true,失败为false
     */
    public abstract boolean BFSearch(JigsawNode bNode, JigsawNode eNode);

    /**
     *（Demo+实验二）启发式搜索。访问节点数大于29000个则认为搜索失败。
     * 函数结束后：searchedNodesNum记录了访问过的节点数；
     *           solutionPath记录了解路径。
     * @param bNode - 初始状态节点
     * @param eNode - 目标状态节点
     * @return 搜索成功返回true,失败返回false
     */
    public final boolean ASearch(JigsawNode bNode, JigsawNode eNode) {

        this.visitedList = new HashSet<>(1000);
        this.exploreList = new PriorityQueue<>(500, new Comparator<JigsawNode>() {
            @Override
            public int compare(JigsawNode a, JigsawNode b) {
                if (a.getEstimatedValue() < b.getEstimatedValue()) {
                    return -1;
                } else if (a.getEstimatedValue() > b.getEstimatedValue()) {
                    return 1;
                } else if (a.getNodeDepth() < b.getNodeDepth()) {
                    return -1;
                } else if (a.getNodeDepth() > b.getNodeDepth()) {
                    return 1;
                }
                return 0;
            }
        });

        this.beginJNode = new JigsawNode(bNode);
        this.endJNode = new JigsawNode(eNode);
        this.currentJNode = null;

        // 访问节点数大于29000个则认为搜索失败
        final int MAX_NODE_NUM = 29000;
        final int DIRS = 4;

        // 重置求解标记
        this.searchedNodesNum = 0;
        this.solutionPath = null;

        // (1)将起始节点放入exploreList中
        this.visitedList.add(this.beginJNode);
        this.exploreList.add(this.beginJNode);

        // (2) 如果exploreList为空，或者访问节点数大于MAX_NODE_NUM个，则搜索失败，问题无解;否则循环直到求解成功
        while (this.searchedNodesNum < MAX_NODE_NUM && !this.exploreList.isEmpty()) {
            this.searchedNodesNum++;

            // (2-1)取出exploreList的第一个节点N，置为当前节点currentJNode
            //      若currentJNode为目标节点，则搜索成功，计算解路径，退出
            this.currentJNode = this.exploreList.poll();
            if (this.currentJNode.equals(eNode)) {
                this.getPath();
                break;
            }

            // 记录并显示搜索过程
            // System.out.println("Searching.....Number of searched nodes:" + searchedNodesNum +
            //     "    Est:" + this.currentJNode.getEstimatedValue() +
            //     "    Current state:" + this.currentJNode.toString());

            JigsawNode[] nextNodes = new JigsawNode[]{
                new JigsawNode(this.currentJNode), new JigsawNode(this.currentJNode),
                new JigsawNode(this.currentJNode), new JigsawNode(this.currentJNode)
            };

            // (2-2)寻找所有与currentJNode邻接且未曾被发现的节点，将它们按代价估值从小到大排序插入exploreList中
            //         并加入visitedList中，表示已发现
            for (int i = 0; i < DIRS; i++) {
                if (nextNodes[i].move(i) && !this.visitedList.contains(nextNodes[i])) {
                    JigsawNode tempJNode = new JigsawNode(nextNodes[i]);
                    this.estimateValue(tempJNode);
                    nextNodes[i].setEstimatedValue(tempJNode.getEstimatedValue());
                    this.visitedList.add(nextNodes[i]);
                    this.exploreList.add(nextNodes[i]);
                }
            }
        }

        System.out.println("Jigsaw AStar Search Result:");
        System.out.println("Begin state:" + this.getBeginJNode().toString());
        System.out.println("End state:" + this.getEndJNode().toString());
        // System.out.println("Solution Path: ");
        // System.out.println(this.getSolutionPath());
        System.out.println("Total number of searched nodes:" + this.getSearchedNodesNum());
        System.out.println("Depth of the current node is:" + this.getCurrentJNode().getNodeDepth());
        return this.isCompleted();
    }

    /**
     *（Demo+实验二）计算并修改状态节点jNode的代价估计值:f(n)。
     * 如 f(n) = s(n). s(n)代表后续节点不正确的数码个数
     * @param jNode - 要计算代价估计值的节点；此函数会改变该节点的estimatedValue属性值。
     */
    public abstract void estimateValue(JigsawNode jNode);

}
