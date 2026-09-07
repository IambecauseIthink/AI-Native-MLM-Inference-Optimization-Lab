# Paper · 标题

状态：unread / analyzed / prototype / integrated / measured / rejected。作者、年份、原文、代码、commit、阅读日期。

## Bottleneck and mechanism

1. 到底解决什么瓶颈？
2. 为什么在真实业务中重要，占端到端多少比例？
3. baseline 是什么？必须另列当前 vLLM baseline。
4. baseline 是否公平：优化程度、版本、资源与精度？
5. workload 是否真实，是否人为高缓存命中/短输出？
6. hardware、GPU 数、拓扑、驱动？
7. batch/concurrency/arrival rate？
8. 输入、视觉和输出 token 分布及 cap？
9. 优化 latency 还是 throughput？测量边界？
10. quality 是否下降？数据与指标能否覆盖业务长尾？
11. 为什么有效？减少 FLOPs/bytes/等待的哪一项？
12. 工作在 model/runtime/scheduler/memory/kernel/serving 哪层？
13. vLLM 是否已有类似机制？固定 commit 下重叠与差异是什么？
14. 接入 vLLM 需要改哪些路径？CUDA Graph、分页、batch、TP、多模态是否兼容？
15. 实验缺了什么消融？哪个结果能推翻作者解释？
16. 相对当前 vLLM 的净收益、维护成本和 no-go 条件？

## Evidence table

| Claim | 原文页/图/表 | 条件 | 自己的验证 | 状态 |
|---|---|---|---|---|
| 待填写 | 待填写 | 待填写 | not-run | unverified |

## Transfer plan

机制 prototype → correctness → vLLM 集成 → 同协议 benchmark → 质量切片 → SLO → go/no-go。把论文报告的数字与自己的复现分开。

## My judgment

研究者先写判断；AI 给出最强反例；根据证据修订。
