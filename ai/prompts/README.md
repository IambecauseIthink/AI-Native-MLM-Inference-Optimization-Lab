# Prompt library

## Source navigator

针对【问题】，在【repo+commit】定位最短调用链。输出 symbol、路径、输入输出、控制分支与证据；区分源码存在和运行时生效。不要通读所有文件，不猜行号。列出可以推翻解释的观测。

## Bottleneck reviewer

我的预测是【X→Y，因为Z】。给出 compute、memory、communication、queue 四种竞争解释；按最小成本设计区分实验。缺少硬件或 shape 信息时标为 unknown。

## Benchmark engineer

依据【冻结协议】，实现收集和验证，不更改样本、cap、并发或质量阈值。保留错误和完整样本；输入、输出、总 TPS 分列；合成数据明确 synthetic。提供验证缺样本/错误/不可比 cohort 的测试。

## Paper transfer reviewer

比较【论文+源码】与【当前 vLLM commit】。定位修改层、重叠优化、batch/cache/graph/TP 兼容性、最小 prototype 和 no-go 条件。所有性能结论都要求同协议 vLLM baseline。

## Reflection coach

先要求我解释结果的因果链，再提出最强反例。不要替我写最终判断；列出下一条最便宜的证据。
