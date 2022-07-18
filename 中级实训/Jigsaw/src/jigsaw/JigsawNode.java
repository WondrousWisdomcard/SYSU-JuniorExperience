package jigsaw;

import java.io.IOException;

/**
 * 拼图游戏的数据结构，描述了拼图游戏的节点状态和节点操作
 * @author abe
 *
 */
public class JigsawNode {
    // private static final int dimension = 3;  // 拼图的维数
    private static final int dimension = 5;     // 拼图的维数 5*5
    private int[] nodesState;                   // 拼图状态：第一位存储空白格的位置；其他各存储对应格子中的数值。
    private int nodeDepth;                      // 从初始状态到达此状态的步数
    private JigsawNode parent;                  // 到达此状态的上一个拼图状态，用于获取解路径
    private int estimatedValue;                 // 代价估计值

    /**
     * JigsawNode构造函数，用以新建一个节点
     * @param data - 节点状态，即一个N*N+1的一维数组（N为拼图维数）。第1位代表空白格所处位置，其余N*N位分别代表每一格中所放方块的数值（按照先行后列排序）。
     */
    public JigsawNode(int[] data) {
        if(data.length == this.dimension*dimension+1){
            this.nodesState = new int[data.length];
            for (int i = 0; i < this.nodesState.length; i++)
                this.nodesState[i] = data[i];
            this.nodeDepth = 0;
            this.parent = null;
            this.estimatedValue = 0;
        } else
            System.out.println("传入参数错误：当前的节点维数为3.请传入长度为" + (dimension * dimension + 1)
                    + "的节点状态数组，或者调整Jigsaw类中的节点维数dimension");
    }

    /**
     * JigsawNode构造函数，创建一个与输入参数相同的节点
     * @param jNode - 用以复制的节点
     */
    public JigsawNode(JigsawNode jNode) {
        this.nodesState = new int[dimension * dimension + 1];
        this.nodesState = (int[]) jNode.nodesState.clone();
        this.nodeDepth = jNode.nodeDepth;
        this.parent = jNode.parent;
        this.estimatedValue = jNode.estimatedValue;
    }

    /**
     * 获取拼图维度
     * @return dimension - 当前拼图维度
     */
    public static int getDimension() {
        return dimension;
    }

    /**
     * 获取节点状态，即一个N*N+1的一维数组。第1位代表空白格所处位置，其余N*N位分别代表每一格中所放方块的数值（按照先行后列排序）。
     * @return nodesState - 节点状态数组
     */
    public int[] getNodesState() {
        return nodesState;
    }

    /**
     * 获取本节点的节点深度，即从初始状态到达此状态的移动步数
     * @return nodeDepth - 节点深度
     */
    public int getNodeDepth() {
        return nodeDepth;
    }

    /**
     * 获取节点的父节点，即到达此节点的上一个节点
     * @return parent - 父节点
     */
    public JigsawNode getParent() {
        return parent;
    }

    /**
     * 获取节点的代价估计值
     * @return estimatedValue - 节点的代价估计值
     */
    public int getEstimatedValue() {
        return estimatedValue;
    }

    /**
     * 设置节点的代价估计值
     * @param estimatedValue - 输入的代价估计值
     */
    public void setEstimatedValue(int estimatedValue) {
        this.estimatedValue = estimatedValue;
    }

    /**
     * 初始化节点的代价估值estimatedValue、节点深度nodeDepth和父节点parent。用与打散拼图操作scatter之后。
     *
     */
    public void setInitial() {
        this.estimatedValue = 0;
        this.nodeDepth = 0;
        this.parent = null;
    }

    /**
     * 比较两个拼图状态，用于检测一个节点是否为目标节点
     * @param obj - JigsawNode类实例，用于与当前节点进行比较的节点
     * @return 状态相同则返回true，否则返回false
     */
    @Override
    public boolean equals(Object obj) {
        for (int i = 0; i < this.nodesState.length; i++) {
            if (this.nodesState[i] != ((JigsawNode) obj).nodesState[i]) {
                return false;
            }
        }
        return true;
    }

    /**
     * Generates a hash code.
     * @return a hash code for this node
     */
    @Override
    public int hashCode() {
        String str = new String();
        for (int index = dimension * dimension; index > 0; index--) {
            str += this.nodesState[index];
        }
        return str.hashCode();
    }

    /**
     * Returns true if this node is valid.
     * @return true if this node is valid
     */
    public boolean isValid() {
        if (this.nodesState == null || this.nodesState.length != (dimension * dimension + 1)
            || this.nodesState[0] < 0 || this.nodesState[0] >= this.nodesState.length
            || this.nodesState[this.nodesState[0]] != 0) {
            return false;
        }
        boolean[] has = new boolean[dimension * dimension];
        for (int i = dimension * dimension; i > 0; i--) {
            if (this.nodesState[i] < 0 || this.nodesState[i] >= has.length) {
                return false;
            }
            has[this.nodesState[i]] = true;
        }
        for (int i = has.length - 1; i >= 0; i--) {
            if (!has[i]) {
                return false;
            }
        }
        return true;
    }

    /**
     * 获取表示当前拼图状态的字符串文本，以一维数组形式显示
     * @return String 表示当前拼图状态的字符串文本（一维数组形式）
     */
    public String toString() {
        String str = new String();
        str += "{" + this.nodesState[0];
        for(int index = 1; index <= dimension * dimension; index++)
            str += "," + this.nodesState[index];
        str += "}";
        return str;
    }

    /**
     * 获取表示当前拼图状态的字符串文本，以行列矩阵形式显示
     * @return String 表示当前拼图状态的字符串文本（行列矩阵形式）
     */
    public String toMatrixString() {
        String str = new String();
        for (int x = 1,index = 1; x <= dimension; x++) {
            for (int y = 1; y <= dimension; y++,index++){
                str += this.nodesState[index] + "  ";
            }
            str += "\n";
        }
        return str;
    }

    /**
     * 探测当前状态中空白格的可移动方位
     *
     * @return 返回一个四位数组，1到4位分别代表空白格是否能向上、下、左、右移动。 值为1时代表该方向可移动，值为0时代表该方向不可移动。
     */
    public int[] canMove() {
        int[] movable = new int[] { 0, 0, 0, 0 };
        if (this.nodesState[0] > dimension
                && this.nodesState[0] <= dimension * dimension)
            movable[0] = 1; // 空白格可向上移
        if (this.nodesState[0] >= 1
                && this.nodesState[0] <= dimension * (dimension - 1))
            movable[1] = 1; // 空白格可向下移
        if (this.nodesState[0] % dimension != 1)
            movable[2] = 1; // 空白格可向左移
        if (this.nodesState[0] % dimension != 0)
            movable[3] = 1; // 空白格可向右移
        return movable;
    }

    /**
     * 探测当前状态中空白格能否向上移动
     * @return 能向上移动则返回true,否则返回false
     */
    public boolean canMoveEmptyUp() {
        return (this.nodesState[0] > dimension && this.nodesState[0] <= dimension
                * dimension);
        // 如果空白格不在第一行则可向上移动
    }

    /**
     * 探测当前状态中空白格能否向下移动
     * @return 能向下移动则返回true,否则返回false
     */
    public boolean canMoveEmptyDown() {
        return (this.nodesState[0] >= 1 && this.nodesState[0] <= dimension
                * (dimension - 1));
        // 如果空白格不在最后一行则可向下移动
    }

    /**
     * 探测当前状态中空白格能否向左移动
     * @return 能向左移动则返回true,否则返回false
     */
    public boolean canMoveEmptyLeft() {
        return (this.nodesState[0] % dimension != 1);
        // 如果空白格不在第一列则可向左移动
    }

    /**
     * 探测当前状态中空白格能否向右移动
     * @return 能向右移动则返回true,否则返回false
     */
    public boolean canMoveEmptyRight() {
        return (this.nodesState[0] % dimension != 0);
        // 如果空白格不在最后一列则可向右移动
    }

    /**
     * 向某一方向移动当前拼图状态中的空白格
     * @param direction - 方向标记：0为向上，1为向下，2为向左，3为向右
     * @return 移动成功返回true，失败返回false
     */
    public boolean move(int direction) {
        switch (direction) {
        case 0:
            return this.moveEmptyUp();
        case 1:
            return this.moveEmptyDown();
        case 2:
            return this.moveEmptyLeft();
        case 3:
            return this.moveEmptyRight();
        default:
            return false;
        }
    }

    /**
     * 向上移动当前拼图状态中的空白格
     * @return 移动成功返回true，失败返回false
     */
    public boolean moveEmptyUp() {
        int emptyPos = this.nodesState[0];
        int emptyValue = this.nodesState[emptyPos];
        if (this.nodesState[0] > dimension
                && this.nodesState[0] <= dimension * dimension) {
            this.parent = new JigsawNode(this);
            this.nodeDepth++;

            this.nodesState[emptyPos] = this.nodesState[emptyPos - dimension];
            this.nodesState[emptyPos - dimension] = emptyValue;
            this.nodesState[0] = emptyPos - dimension;

            return true;
        }
        return false;
    }

    /**
     * 向下移动当前拼图状态中的空白格
     * @return 移动成功返回true，失败返回false
     */
    public boolean moveEmptyDown() {
        int emptyPos = this.nodesState[0];
        int emptyValue = this.nodesState[emptyPos];
        if (this.nodesState[0] >= 1
                && this.nodesState[0] <= dimension * (dimension - 1)) {
            this.parent = new JigsawNode(this);
            ;
            this.nodeDepth++;

            this.nodesState[emptyPos] = this.nodesState[emptyPos + dimension];
            this.nodesState[emptyPos + dimension] = emptyValue;
            this.nodesState[0] = emptyPos + dimension;
            return true;
        }
        return false;
    }

    /**
     * 向左移动当前拼图状态中的空白格
     * @return 移动成功返回true，失败返回false
     */
    public boolean moveEmptyLeft() {
        int emptyPos = this.nodesState[0];
        int emptyValue = this.nodesState[emptyPos];
        if (this.nodesState[0] % dimension != 1) {
            this.parent = new JigsawNode(this);
            ;
            this.nodeDepth++;

            this.nodesState[emptyPos] = this.nodesState[emptyPos - 1];
            this.nodesState[emptyPos - 1] = emptyValue;
            this.nodesState[0] = emptyPos - 1;
            return true;
        }
        return false;
    }

    /**
     * 向右移动当前拼图状态中的空白格
     * @return 移动成功返回true，失败返回false
     */
    public boolean moveEmptyRight() {
        int emptyPos = this.nodesState[0];
        int emptyValue = this.nodesState[emptyPos];
        if (this.nodesState[0] % dimension != 0) {
            this.parent = new JigsawNode(this);
            ;
            this.nodeDepth++;

            this.nodesState[emptyPos] = this.nodesState[emptyPos + 1];
            this.nodesState[emptyPos + 1] = emptyValue;
            this.nodesState[0] = emptyPos + 1;
            return true;
        }
        return false;
    }

}
