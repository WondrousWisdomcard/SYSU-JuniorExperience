Apriori算法（前两年数据）筛选后结果：（有效关系对和置信度）

* 黄金：
  ['PM', 'BM', 0.556]
  ['PS', 'BM', 0.625]
  ['PS PM', 'BM', 0.625]
  ['NM', 'SM', 0.545]
  ['NS', 'SM', 0.545]
  ['NM NS', 'SM', 0.545]
* 比特币：
  ['NL', 'BB', '0.472']
  ['PL', 'SB', 0.384]

经过对前两年的学习，得到以下规则：

令大卖, 中卖, 小卖, 持平, 小买, 中买, 大买 依次对应：$c_i= [-4\omega, -2\omega, -\omega, 0, \omega, 2\omega, 4\omega]$

* 黄金：
  * 大涨时选择中买
  * 中涨时选择中买
  * 大跌时选择中卖
  * 中跌时选择中卖
  * 得到模糊系统输出：$ed(x) = \frac{2\omega\mu_{pl}(x) + 2\omega\mu_{pm}(x) -2\omega\mu_{nl}(x) -2\omega \mu_{nm}(x)}{\mu_{pl}(x) + \mu_{pm}(x) + \mu_{nl}(x) + \mu_{nm}(x)}$

* 比特币：
  * 大涨时选择大买
  * 大跌时选择大卖
  * 得到模糊系统输出：$ed(x) = \frac{4\omega \mu_{pl}(x) - 4\omega \mu_{nl}(x)}{\mu_{pl}(x) + \mu_{nl}(x)}$