# 04 · 一个长请求，为什么拖慢其他人？

**这次只解决：两个请求正在逐 token 输出，一个长 prompt 加入。先给谁安排 GPU 工作，会改变谁的等待？**

用时 30–45 分钟，可随时暂停。让助手说“带我学第 04 课”，由助手先解释例子，再分步展开。无需先读完教材，不安装模型。

## 先理解这个例子

客户端并发是同时在途请求数；实际 batch 是某轮被选中的工作。token budget 控制一轮能安排多少 token，max_num_seqs 控制序列数量，二者不同。KV 空间不够时，runtime 还可能抢占请求并在之后重算或恢复，因此有计算预算也不保证能立即运行。continuous batching 可以在迭代间更新活跃集合；chunking 切开长 prefill，让其他工作有被安排的机会。

## 做一个预测，然后操作

保持 budget=8，只关掉 decode_first，短请求的完成工作刻度是否改变？再单独比较 chunked。

允许回答“不确定，因为……”。在仓库根目录运行；每次只改变一个条件，恢复默认后再试下一个：

```bash
python3 scripts/lab.py lesson --id 04
python3 scripts/lab.py lesson --id 04 --set decode_first=0
python3 scripts/lab.py lesson --id 04 --set chunked=0
python3 scripts/lab.py lesson --id 04 --params
```

[交互图源码](../visuals/lesson-04.html) 可由助手直接在对话中展示；不要依赖 VS Code 默认 Markdown 预览执行脚本。可选本地预览方法见 [交互实验说明](../visuals/README.md)。结果始终标明 synthetic/analytical，不是 GPU 实测。

## 用一点原理解释

`教学约束：Σ本轮 token ≤ budget；work ticks=已执行 token 总量。work tick 不是毫秒，不把 prefill/decode 等成本当硬件事实。`

更小 chunk 不保证更快：launch、GEMM 效率、prefill/decode 成本与公平性都会影响结果。

## 带着问题看源码和教材

vLLM **v0.19.0 / 2a69949bdadf0e8942b7a1619b229cb475beef20**；源码导航不是运行证明。

- [Scheduler.schedule](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/sched/scheduler.py#L348) · `vllm/v1/core/sched/scheduler.py` · L348。

读 Scheduler.schedule 开头和 RUNNING 循环。真实 V1 用 num_computed_tokens 与目标 token 数推进，并不是两个独立“prefill/decode 队列”；对照 toy 的显式 phase，指出差异。再搜索 preempted_reqs 看重算/抢占如何进入流程。

教材：[MLSysBook · Batching](https://mlsysbook.ai/vol1/model_serving/model_serving.html)。在 Model Serving 搜索 batching 与 latency-throughput trade-off；静态/dynamic batching 作为对照，再读本课的 token 调度。

## 今天如何结束

回答：若不切分的 prompt 超过 toy budget，为什么例子会停住？这能证明 vLLM 会死锁吗？

在 [进度记录](../progress.md) 留下自己的预测、观察、未知与下一步。读完或跑完不自动等于掌握，不自动进入下一课。

下一步：继续第 05 课：有些 prefill 可以因为缓存而根本不执行。

[远程验证设计](remote.md) · [教师页：带学时再看](teacher.md) · [回到课程入口](../README.md)
