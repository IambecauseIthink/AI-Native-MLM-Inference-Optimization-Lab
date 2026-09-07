# Serving & Scheduling

覆盖主题：static / dynamic / continuous batching / request-level / token-level / priority / admission / queueing / SLO。

## 因果关系

Triton 接入层与内部 vLLM scheduler 是不同层：接入排队、backend 转换、engine token 调度都可贡献延迟。Triton dynamic batching 与 vLLM continuous batching 不能直接视为同一个开关。Triton Inference Server 与 Triton kernel language 也不是同一工具。

固定并发 closed-loop 客户端在响应变慢时自然降低提交速率，不能代表固定到达率的生产流量。open-loop 必须记录计划到达、实际发送、完成、超时和积压，避免协调遗漏使尾延迟看起来过好。

QPS=成功请求/测量墙钟时间；goodput 只计算满足预先定义 SLO 的成功请求。TPOT、TTFT、E2E 的分位数分别计算；P99(TTFT)+P99(decode) 不等于 P99(E2E)。优先级可保护某类请求，却可能使其他请求饥饿。

P/D 分离需衡量 KV 传输、队列、资源池配比与网络；并非拆开就加速。

## Question-driven Source Reading

选择一个主题，记录 Concept → Problem → Naive failure → Design → Source → Experiment → Benchmark → Limitations → Improvement。每个节点回答具体问题，不只是链接。

先看 config/入口，再 `rg` 搜索相关 class/function，跟踪最小调用链。记录 repository、commit、file、symbol、输入输出和实际生效分支；安装版本不同就重新定位。

## 本模块实验入口

负载逐级提高，画成功 QPS、goodput、错误率与 P99 曲线；在固定 SLO 下比较容量。

先写预测、固定条件、失败判据；按 [实验模板](../../templates/experiment.md) 保存。Core 到 designed；真正运行后才填 Results。

## 学会的证据

能解释为什么有效、什么时候无效，以及一个反例。模型结构主题还必须逐项回答：出现原因、解决问题、training、inference、latency、throughput、KV、GPU memory、vLLM support、优化机会。

参考 [来源索引](../sources.md) 与 [Benchmark 合同](../../benchmarks/README.md)。
