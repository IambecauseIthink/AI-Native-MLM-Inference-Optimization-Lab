# 01 · 两个服务，谁真的更快？

**这次只解决：同样 8 个请求，B 更快处理完全部请求，但是中位请求体验更差。选 A 还是 B？**

用时 30–45 分钟，可随时暂停。让助手说“带我学第 01 课”，由助手先解释例子，再分步展开。无需先读完教材，不安装模型。

## 先理解这个例子

先画一条时间线：提交 → 排队 → 第一个 token → 后续 token → 完成。TTFT 包含提交后的等待；TPOT 描述首 token 后的生成间隔，只有一个 token 时未定义。QPS 统计整个窗口完成多少请求，不能把一个请求的延迟倒数当高并发 QPS。

## 做一个预测，然后操作

先看默认 A/B 的时间线，再预测：只把 B 的 batch 从 8 改成 4，哪些请求要多等一批？

允许回答“不确定，因为……”。在仓库根目录运行；每次只改变一个条件，恢复默认后再试下一个：

```bash
python3 scripts/lab.py lesson --id 01
python3 scripts/lab.py lesson --id 01 --set batch=4
python3 scripts/lab.py lesson --id 01 --set service_ms=1000
python3 scripts/lab.py lesson --id 01 --params
```

[交互图源码](../visuals/lesson-01.html) 可由助手直接在对话中展示；不要依赖 VS Code 默认 Markdown 预览执行脚本。可选本地预览方法见 [交互实验说明](../visuals/README.md)。结果始终标明 synthetic/analytical，不是 GPU 实测。

## 用一点原理解释

`QPS = 成功请求 / 窗口秒；TTFT = 首 token − 提交；TPOT = (末 token − 首 token)/(输出数 − 1)；E2E = 完成 − 提交。`

QPS 较高并不能保证所有分位延迟都更小；本例 B 的 E2E P50 更差，但 P99 更好。

## 带着问题看源码和教材

vLLM **v0.19.0 / 2a69949bdadf0e8942b7a1619b229cb475beef20**；源码导航不是运行证明。

- [AsyncLLM.generate](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/engine/async_llm.py#L529) · `vllm/v1/engine/async_llm.py` · L529。
- [AsyncLLM.add_request](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/engine/async_llm.py#L288) · `vllm/v1/engine/async_llm.py` · L288。

先打开 generate，只找 add_request、输出迭代和取消处理；再打开 add_request，看请求如何进入 engine。它不是 HTTP 路由全过程，也不能只凭这段函数断言实际 kernel。

教材：[MLSysBook · Performance Metrics](https://mlsysbook.ai/vol1/benchmarking/benchmarking.html)。只带着“指标的计时起点、终点和分母是什么”阅读；再到 Model Serving 搜索 latency-throughput trade-off。

## 今天如何结束

回答：如果用户更在意 TTFT，而离线任务更在意排空时间，两者能选择不同配置吗？

在 [进度记录](../progress.md) 留下自己的预测、观察、未知与下一步。读完或跑完不自动等于掌握，不自动进入下一课。

下一步：继续第 02 课，解释 batch 为什么可能提高单位权重搬运的收益。

[远程验证设计](remote.md) · [教师页：带学时再看](teacher.md) · [回到课程入口](../README.md)
