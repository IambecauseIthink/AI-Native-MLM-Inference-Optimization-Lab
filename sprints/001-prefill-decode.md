# Sprint 001 · Prefill 为什么与 Decode 不同？

状态：designed。先写预测，再让 AI 审阅。

## Core

**Theory**：阅读 [因果模型](../docs/00-inference-overview/README.md)。画出单请求与四请求的调度循环。解释权重复用、KV 读取和队列分别改变什么。

**Source**：在远程/外部固定 commit 的 vLLM checkout 中搜索 `class Scheduler`、`def schedule`、`execute_model`。记录路径、symbol、调用者和运行证据；不要猜测行号。源码克隆不是运行模型。

**Experiment**：设计两组：固定 output cap/concurrency 扫描输入 512/2048/8192；固定输入/cap 扫描 concurrency 1/4/16。分别预测 TTFT、TPOT、QPS、显存变化。固定采样与 EOS 策略，记录实际完成 token 数。

**Reflection**：如果 batch 增大但 QPS 不增，列出 memory、compute、KV capacity、CPU/queue 四种竞争解释，给出能区分它们的证据。

## 可立即运行

```bash
python3 scripts/lab.py kv --layers 32 --kv-heads 8 --head-dim 128 --tokens 8192 --batch 4 --bytes 2
```

预期 raw KV 为 4 GiB。这是假设所有 32 层均为 full attention 的解析值，不是某个 Qwen 的实测内存；不含权重、激活、分页浪费、workspace 和线性状态。

## Stretch

远程执行冻结的输入矩阵，用独立 profiler run 观察 GEMM 时间与 decode 每步的权重/KV 读取。不能以 nvidia-smi 利用率单独证明 bandwidth-bound。

## 验收

- [ ] 自己写出三条预测和适用前提。
- [ ] 一个固定 commit 的源码调用链。
- [ ] 一份冻结的实验设计，未运行则保持 designed。
- [ ] 一个反例及下一步证伪实验。
