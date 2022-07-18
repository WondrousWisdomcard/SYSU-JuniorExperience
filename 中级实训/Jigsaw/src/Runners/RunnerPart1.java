package Runners;

import java.io.IOException;

import jigsaw.Jigsaw;
import jigsaw.JigsawNode;
import solution.Solution;

public class RunnerPart1 {
    /**
     * 演示脚本-1
     * 实验任务一：利用广度优先搜索，求指定3*3拼图（8-数码问题）的最优解
     * 要求：不修改脚本内容，程序能够运行，且得出预期结果
     * @param args
     * @throws IOException
     */
    public static void main(String[] args) throws IOException {
        // 检查节点维数是否为3
        if (JigsawNode.getDimension() != 3) {
            System.out.print("节点维数不正确，请将JigsawNode类的维数dimension改为3");
            return;
        }

	//JigsawNode startNode = new JigsawNode(new int[]{8,2,8,3,1,6,4,7,0,5});
	//JigsawNode destNode = new JigsawNode(new int[]{5,1,2,3,8,0,4,7,6,5});

        // 生成目标状态destNode：{9,1,2,3,4,5,6,7,8,0}
       	JigsawNode destNode = new JigsawNode(new int[]{9,1,2,3,4,5,6,7,8,0});
        // JigsawNode destNode = new JigsawNode(new int[]{2,1,0,2,7,5,4,6,3,8});
        // 生成指定初始状态startNode：{5,1,5,2,7,0,4,6,3,8}
        JigsawNode startNode = new JigsawNode(new int[]{5,1,5,2,7,0,4,6,3,8});

        // 生成jigsaw对象：设置初始状态节点startNode和目标状态节点destNode
        Jigsaw j = new Solution();

        // 执行广度优先搜索算法
        j.BFSearch(startNode, destNode);
    }
}
