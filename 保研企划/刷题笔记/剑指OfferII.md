[toc]

## Day 01(36) 图

1. [**剑指 Offer II 105. 岛屿的最大面积**](https://leetcode.cn/problems/ZL6zAn/) 给定一个由 `0` 和 `1` 组成的非空二维数组 `grid` ，用来表示海洋岛屿地图。一个 **岛屿** 是由一些相邻的 `1` (代表土地) 构成的组合，这里的「相邻」要求两个 `1` 必须在水平或者竖直方向上相邻。你可以假设 `grid` 的四个边缘都被 `0`（代表水）包围着。找到给定的二维数组中最大的岛屿面积。如果没有岛屿，则返回面积为 `0` 。

   ```c++
   class Solution {
   private:
       int res = 0, tmp = 0;
       int n = 0, m = 0;
   public:
       void travel(vector<vector<int>>& grid, vector<vector<int>>& vis, int i, int j){
           if(i >= 0 && i < n && j >= 0 && j < m && grid[i][j] == 1 && vis[i][j] == 0){
               vis[i][j] = 1;
               tmp++;
               travel(grid, vis, i + 1, j);
               travel(grid, vis, i, j + 1);
               travel(grid, vis, i - 1, j);
               travel(grid, vis, i, j - 1);
           }
       } 
       int maxAreaOfIsland(vector<vector<int>>& grid) {
           n = grid.size();
           m = grid[0].size();
           vector<vector<int>> vis(n, vector<int>(m, 0));
           for(int i = 0; i < n; i++){
               for(int j = 0; j < m; j++){
                   tmp = 0;
                   travel(grid, vis, i, j);
                   if(res < tmp){
                       res = tmp;
                   }
               }
           }
           return res;
       }
   };
   ```

2. [**剑指 Offer II 106. 二分图**](https://leetcode.cn/problems/vEAB3K/) 邻接表判断二部图，图不一定为连接图

   ``` c++
   class Solution {
   private:
       int n = 0;
       bool res = true;
   public:
       void coloring(vector<vector<int>>& graph, vector<int>& colors, int i){
           if(colors[i] != 0){
               int m = graph[i].size();
               int rb = colors[i];
               for(int j = 0; j < m; j++){
                   if(colors[graph[i][j]] == 0){
                       colors[graph[i][j]] = -rb;
                       coloring(graph, colors, graph[i][j]);
                   }
                   else if(colors[graph[i][j]] == rb){
                       res = false;
                       return;
                   }
               }
           }
       }
       bool isBipartite(vector<vector<int>>& graph) {
           n = graph.size();
           vector<int> colors(n, 0);
           for(int i = 0; i < n; i++){
               if(colors[i] == 0){
                   colors[i] = 1;
                   coloring(graph, colors, i);
               }
           }
           return res;
       }
   };
   ```

3. [**剑指 Offer II 107. 矩阵中的距离**](https://leetcode.cn/problems/2bCMpM/)

   * 我的思路：既不是 DFS 也不是 BFS，而是一种粗暴的矩阵迭代

   ```
   class Solution {
   private:
       int n = 0, m = 0;
   public:
       vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
           n = mat.size();
           m = mat[0].size();
           vector<vector<int>> dis(n, vector<int>(m, INT_MAX));
           int l = 0;
           bool stop = true;
           while(stop){
               stop = false;
               for(int i = 0; i < n; i++){
                   for(int j = 0; j < m; j++){
                       if(mat[i][j] == 0 && l == 0){
                           stop = true;
                           dis[i][j] = 0;
                       }
                       if(dis[i][j] == l){
                           if(i - 1 >= 0 && dis[i - 1][j] > l + 1){
                               stop = true;
                               dis[i - 1][j] = l + 1;
                           }
                           if(i + 1 < n && dis[i + 1][j] > l + 1){
                               stop = true;
                               dis[i + 1][j] = l + 1;
                           }
                           if(j - 1 >= 0 && dis[i][j - 1] > l + 1){
                               stop = true;
                               dis[i][j - 1] = l + 1;
                           }
                           if(j + 1 < m && dis[i][j + 1] > l + 1){
                               stop = true;
                               dis[i][j + 1] = l + 1;
                           }
                       }
                   }
               }
               l++;
           }
           return dis;
       }
   };
   ```

   * **正确的 BFS 思路：将所有的 0 （超级零）添加进初始队列中，再进行一趟 BFS，而不是对每个节点单独进行 BFS**

   ```c++
   class Solution {
   private:
       static constexpr int dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
   
   public:
       vector<vector<int>> updateMatrix(vector<vector<int>>& matrix) {
           int m = matrix.size(), n = matrix[0].size();
           vector<vector<int>> dist(m, vector<int>(n));
           vector<vector<int>> seen(m, vector<int>(n));
           queue<pair<int, int>> q;
           // 将所有的 0 添加进初始队列中
           for (int i = 0; i < m; ++i) {
               for (int j = 0; j < n; ++j) {
                   if (matrix[i][j] == 0) {
                       q.emplace(i, j);
                       seen[i][j] = 1;
                   }
               }
           }
           // 广度优先搜索
           while (!q.empty()) {
               auto [i, j] = q.front();
               q.pop();
               for (int d = 0; d < 4; ++d) {
                   int ni = i + dirs[d][0];
                   int nj = j + dirs[d][1];
                   if (ni >= 0 && ni < m && nj >= 0 && nj < n && !seen[ni][nj]) {
                       dist[ni][nj] = dist[i][j] + 1;
                       q.emplace(ni, nj);
                       seen[ni][nj] = 1;
                   }
               }
           }
   
           return dist;
       }
   };
   ```

   * **最优方法：动态规划，两趟动态规划，分别限制方向为 从左上到右下 和 从右下到左上。**

   ``` c++
   class Solution {
   public:
       vector<vector<int>> updateMatrix(vector<vector<int>>& matrix) {
           int m = matrix.size(), n = matrix[0].size();
           // 初始化动态规划的数组，所有的距离值都设置为一个很大的数
           vector<vector<int>> dist(m, vector<int>(n, INT_MAX / 2));
           // 如果 (i, j) 的元素为 0，那么距离为 0
           for (int i = 0; i < m; ++i) {
               for (int j = 0; j < n; ++j) {
                   if (matrix[i][j] == 0) {
                       dist[i][j] = 0;
                   }
               }
           }
           // 只有 水平向左移动 和 竖直向上移动，注意动态规划的计算顺序
           for (int i = 0; i < m; ++i) {
               for (int j = 0; j < n; ++j) {
                   if (i - 1 >= 0) {
                       dist[i][j] = min(dist[i][j], dist[i - 1][j] + 1);
                   }
                   if (j - 1 >= 0) {
                       dist[i][j] = min(dist[i][j], dist[i][j - 1] + 1);
                   }
               }
           }
           // 只有 水平向右移动 和 竖直向下移动，注意动态规划的计算顺序
           for (int i = m - 1; i >= 0; --i) {
               for (int j = n - 1; j >= 0; --j) {
                   if (i + 1 < m) {
                       dist[i][j] = min(dist[i][j], dist[i + 1][j] + 1);
                   }
                   if (j + 1 < n) {
                       dist[i][j] = min(dist[i][j], dist[i][j + 1] + 1);
                   }
               }
           }
           return dist;
       }
   };
   ```

## Day 02(23) 二分查找

1. [剑指 Offer II 068. 查找插入位置](https://leetcode.cn/problems/N6YdxV/) 给定一个排序的整数数组 nums 和一个整数目标值 target ，请在数组中找到 target ，并返回其下标。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。

2. [剑指 Offer II 069. 山峰数组的顶部](https://leetcode.cn/problems/B1IidL/) 

   ``` c++
   class Solution {
   public:
       int peakIndexInMountainArray(vector<int>& arr) {
           int l = 0, r = arr.size() - 1;
           while(l < r){
               int m = (l + r) / 2;
               if(m < arr.size() && arr[m] < arr[m + 1]){
                   l = m + 1;
               }
               else{
                   r = m;
               }
           }
           return l;
       }
   };
   ```

   
