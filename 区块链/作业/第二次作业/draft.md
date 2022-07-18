重点阅读 “Monoxide: Scale Out Blockchain with Asynchronized Consensus Zones”，2019年由计算机网络顶级学术会议 NSDI 所接收

* 利用分片的思想把区块链划分为多个共识组以提升区块链的可扩展性
* 单一系统分割成一定程度上独立的N个共识组子系统，以线性地提升整个系统的交易处理速度与吞吐量 
* 交易的吞吐量及TPS约为原来的N倍
* 在连弩挖矿这种模式下，矿工算力不会稀释到多个共识组上，使得攻击者集中算力去攻击单个共识组也不能获得优势 

总结与思考： 

* 比特币设计简单，但是它能顺畅运行，背后有什么原因？
* Monoxide 提出的共识机制 与 比特币的共识机制有哪些不一样？
* 思考：连弩挖矿机制存在什么样的潜在问题？

文献： 

* Monoxide: Scale Out Blockchain with Asynchronized Consensus Zones
* Majority Is Not Enough Bitcoin: Mining Is Vulnerable 
* “ Proof-of-Work ” Proves Not to Work; version 0.2

Deadline: 

2周之内提交到如下邮箱: blockchainclass@163.com – 提交格式：学号+姓名.PDF，不要写太长，不要抄袭



**Abstract**

加密货币为匿名在线支付提供了一个很有前途的基础设施。然而，低吞吐量严重阻碍了加密货币系统的可伸缩性和可用性，以满足不断增加的用户和交易数量。实现可伸缩性的另一个障碍是每个节点都需要复制整个网络的通信、存储和状态表示。

在本文中，我们引入了**异步共识区域**，它可以线性扩展区块链系统，而不影响去中心化或安全性。我们通过运行被称为**区域**的单链共识系统的多个独立和并行实例来实现这一点。该共识在每个区域内独立地发生，并将通信最小化，这将对整个网络的工作负载进行分区，并确保随着网络的增长，每个独立节点的负担适中。我们建议使用**最终原子性**来确保跨区域的事务原子性，这样可以在没有两阶段提交协议开销的情况下高效地完成事务。此外，我们提出**Chu-ko-nu挖掘**，以确保每个区域的有效挖掘能力处于整个网络的同一级别，使对任何单个区域的攻击与对整个网络的攻击一样困难。我们的实验结果表明了我们工作的有效性:在一个包括1200个虚拟机的测试台上，支持48000个节点，我们的系统在比特币和以太坊网络上提供1000倍的吞吐量和2000倍的容量。



---

* 比特币设计简单，但是它能顺畅运行，背后有什么原因？
  * 安全机制
  * 激励机制
  * 动态平衡（计算能力与生成区块速度）
* Monoxide 提出的共识机制 与 比特币的共识机制有哪些不一样？
  * 分区
  * Batch 分批
* 思考：连弩挖矿机制存在什么样的潜在问题？
  * 截留攻击

  
  * 冗杂，数据重复 
  * 最终原子性使得交易数目*2
  * However, a larger block size or a smaller block creation interval leads to a higher orphan rate, inducing blocks wasted. （Such behavior matches well with the existing blockchain system ） 
  
  
  
  我们的方法要求跨区域交易可以在单个区域内验证，并通过一步不可撤销的中继交易完成，这并不支持多对多支付等应用程序。
  
  
