# MoE调研

DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale

**提升泛化性能**

- 增加专家数量：消耗更多内存
- 使用Top-K个专家：消耗更多通信量。

**模型压缩的方案**

- 残差MoE：固定一个专家（原密集网络的MLP可以视为第一个专家），只选择第二个专家，基于直觉“用额外的专家来修正第一个专家的表现”——达到只选择一个专家的通信量
- 金字塔残差MoE/PR-MoE：每一层使用不同数量的专家，接近输出的深层次一般学习更客观的特定表示，放更多专家的效果更好。（缩小模型尺寸，达到一样的效果）

![image-20230924173616649](https://s2.loli.net/2023/09/24/1naRoqBw8ciJZ7p.png)

![image-20230924173630228](https://s2.loli.net/2023/09/24/PZzbyL3d4pgQ918.png)

- 结合知识蒸馏MoS：利用知识蒸馏进行减层，减小模型的大小（深度？）和模型计算。教师模型和学生模型都设计为MoE结构的，但是减少学生模型中专家分支中的深度。为防止过拟合/学生模型能力不足，采用分阶段的知识蒸馏（让知识蒸馏比整个训练过程更早停止，逐渐减小它loss的权重）。

  注：PR-MoE+MoS会使得训练内存消耗下降3倍，且保留只选一个专家的通信量，同时保持了模型的准确性。

- 量化



代码实现：deepspeed.moe.layer.MoE API

![image-20230924212728033](https://s2.loli.net/2023/09/24/NGbR5dWMxV1yAps.png)

![image-20230924213719880](https://s2.loli.net/2023/09/24/G3Puao47xTAjc9e.png)

llama+lora+MoE
