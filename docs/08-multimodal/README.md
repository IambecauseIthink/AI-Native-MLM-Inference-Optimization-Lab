# Multimodal Optimization

覆盖主题：vision encoder / visual tokens / token pruning / merging / compression / adaptive resolution / dynamic selection。

## 因果关系

图像经 processor 与 vision encoder 变为视觉表示，再进入语言侧。增加视觉 token 会提高语言 prefill 工作量，并通常增加 full-attention 层的 KV；视觉编码自身的代价需独立计时。混合架构不应将所有层 KV 都按序列线性外推。

减少 visual token 可能损失小字、计数、定位与跨图关系。平均业务指标掩盖罕见但关键切片。token reduction 必须验证 projector 输出、placeholder 数、position IDs、RoPE、mask、缓存键及多图/视频顺序。

Transformers prototype 有收益不代表 vLLM 可部署：runtime 的输入处理、encoder cache、batch packing、shape capture 和分布式路径都可能需要修改。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

固定 processor 和图像集合，扫描分辨率/token budget；分别测 encoder、prefill、decode，并评估 OCR/计数/定位质量。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
