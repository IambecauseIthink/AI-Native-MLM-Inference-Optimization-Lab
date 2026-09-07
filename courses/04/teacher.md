# 04 教师指导 · 一个长请求，为什么拖慢其他人？

## 带学节奏

- 0–5 分钟：讲具体情境“两个请求正在逐 token 输出，一个长 prompt 加入。先给谁安排 GPU 工作，会改变谁的等待？”。先给一个已解释的例子，不连续抛术语或测验。
- 5–10 分钟：共同画出对象/shape/时间线。基础只补学习页的一段，让学员用自己的话指认变量。
- 10–20 分钟：展示默认实验，再询问学习页的一个预测；允许未知。只改一个条件，显示前后结果。
- 20–28 分钟：解释公式与假设，邀请学员指出哪个成本被省略；不要把 toy 数字解释成硬件事实。
- 28–35 分钟：跟读以下真实 symbol，最多打开两个必要调用片段；较长调用链可留到下次。
- 35–45 分钟：做一个反例，记录学员原话、未知与下一步；未经学员明确完成判断，不更新为掌握。

## 结果与递进提示

默认三请求完成，总工作 23 ticks。先服务长 prefill 会拖后短请求。budget=4/8 且关闭 chunked 时，短请求完成后长 prefill 无法放入预算，返回 blocked-budget；这是教学策略边界，不模拟 vLLM 对配置的验证和真实调度。

提示一：先看改变了哪个输入。提示二：指出公式中的对应项。提示三：一起算最小数字，再回到完整例子。不要用“显然”“你应该知道”评价学员。

## 真实实现导航

- [Scheduler.schedule](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/sched/scheduler.py#L348) · `vllm/v1/core/sched/scheduler.py` · L348。

读 Scheduler.schedule 开头和 RUNNING 循环。真实 V1 用 num_computed_tokens 与目标 token 数推进，并不是两个独立“prefill/decode 队列”；对照 toy 的显式 phase，指出差异。再搜索 preempted_reqs 看重算/抢占如何进入流程。

不要把最新文档与固定源码混用；如果实际运行选择了别的 runner/backend，另记证据，不改写这份教学基准。

## 误区与边界

不输出这三个请求的模型 QPS/TTFT。教学 scheduler 没有真实并行 kernel、KV 容量、抢占或多模态预算，不能作为 runtime 替代。

反例：更小 chunk 不保证更快：launch、GEMM 效率、prefill/decode 成本与公平性都会影响结果。

## 理解出口

学员能解释一个预测、指出一个假设、提出一条可以否证解释的观察。未达到时，把困难拆成更小例子，不重复整套讲义。

进度初始为 ready；根据真实对话填写 [progress](../progress.md)。本课远程实验仍是 designed，没有启动 GPU。
