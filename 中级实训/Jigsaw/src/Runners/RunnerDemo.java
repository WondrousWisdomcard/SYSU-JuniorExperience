package Runners;

import java.io.IOException;

import jigsaw.Jigsaw;
import jigsaw.JigsawNode;
import solution.Solution;

public class RunnerDemo {

    /**
     * 演示脚本：启发式搜索-示例算法-求解随机3*3拼图（8-数码问题）
     * @param args
     * @throws IOException
     */
    public static void main(String[] args) throws IOException {
        // 检查节点维数是否为3
        if (JigsawNode.getDimension() != 3) {
            System.out.print("节点维数不正确，请将JigsawNode类的维数dimension改为3");
            return;
        }

        // 生成目标状态对象destNode: {9,1,2,3,4,5,6,7,8,0}
        JigsawNode destNode = new JigsawNode(new int[]{9,1,2,3,4,5,6,7,8,0});

        // 生成随机初始状态对象startNode：将目标状态打散，生成可解的随机初始状态
        // JigsawNode startNode = Jigsaw.scatter(destNode, 1000);
        JigsawNode startNode = new JigsawNode(new int[]{5,1,5,2,7,0,4,6,3,8});
        // 生成jigsaw对象：设置初始状态节点startNode和目标状态节点destNode
        Jigsaw jigsaw = new Solution();

        // 执行启发式搜索示例算法
        jigsaw.ASearch(startNode, destNode);
    }

}
