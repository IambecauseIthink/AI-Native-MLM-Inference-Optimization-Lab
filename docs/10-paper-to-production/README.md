# Paper → vLLM → Production

覆盖主题：target / baseline / compatibility / prototype / integration / ablation / quality / feasibility。

## 因果关系

先标注论文修改发生在 model、runtime、scheduler、memory、kernel 还是 serving，再定位生产对应层。比较对象必须包含同版本同 workload 的 vLLM baseline；Transformers 仅作为机制或复现辅助基线。

把论文收益拆成算法、kernel、batch、量化与输入变化。公平比较必须控制 hardware、资源数、数据、token cap、质量与测量边界。无法迁移的收益仍可解释机制，但不能声称生产提升。

迁移路线：最小 eager prototype→logits/任务质量检查→固定 commit vLLM 接入→stream/cancel/batch/long-context 测试→真实负载→质量合格后 Pareto→灰度、回滚与监测。论文比 naive 快 20%，不说明比当前 vLLM 快。

Go/no-go 同时考量维护成本、升级冲突、许可证、尾延迟、失败恢复与质量；证据支持的 no-go 也是成功研究产物。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

固定协议比较 vLLM、论文 prototype、vLLM+方法；消融算法与 kernel 的独立贡献。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
