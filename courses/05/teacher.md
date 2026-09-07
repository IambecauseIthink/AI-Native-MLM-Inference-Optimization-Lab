# 05 教师指导 · 相似提示词，为什么没有缓存收益？

## 带学节奏

- 0–5 分钟：讲具体情境“两个 prompt 语义非常相似，但第一行的时间戳不同。为什么可能没有 prefix cache 命中？”。先给一个已解释的例子，不连续抛术语或测验。
- 5–10 分钟：共同画出对象/shape/时间线。基础只补学习页的一段，让学员用自己的话指认变量。
- 10–20 分钟：展示默认实验，再询问学习页的一个预测；允许未知。只改一个条件，显示前后结果。
- 20–28 分钟：解释公式与假设，邀请学员指出哪个成本被省略；不要把 toy 数字解释成硬件事实。
- 28–35 分钟：跟读以下真实 symbol，最多打开两个必要调用片段；较长调用链可留到下次。
- 35–45 分钟：做一个反例，记录学员原话、未知与下一步；未经学员明确完成判断，不更新为掌握。

## 结果与递进提示

默认 32 token、block8：请求1冷启动0命中，请求2共享16命中16，后续完全重复命中24，最后一块为 logits 重算。容量2只保留尾部块，toy 连续前缀查找因此失败。

提示一：先看改变了哪个输入。提示二：指出公式中的对应项。提示三：一起算最小数字，再回到完整例子。不要用“显然”“你应该知道”评价学员。

## 真实实现导航

- [KVCacheManager.get_computed_blocks](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/kv_cache_manager.py#L176) · `vllm/v1/core/kv_cache_manager.py` · L176。
- [BlockPool.get_cached_block](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/block_pool.py#L183) · `vllm/v1/core/block_pool.py` · L183。
- [BlockPool.cache_full_blocks](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/block_pool.py#L210) · `vllm/v1/core/block_pool.py` · L210。

get_computed_blocks 中核对 skip_reading_prefix_cache 与 prompt_length−1；再看 BlockPool.get_cached_block 的 group 标识和 cache_full_blocks 的完整块。toy 用完整前缀 tuple，不是实际 hash/引用计数算法。

不要把最新文档与固定源码混用；如果实际运行选择了别的 runner/backend，另记证据，不改写这份教学基准。

## 误区与边界

本实验只数可复用 tokens，不把命中率乘以 E2E 当加速比；真实 block 生命周期、并发引用计数、驱逐策略与 toy LRU 不同。

反例：一次 warm、高重复实验不能代表生产平均收益；应用层改模板、salt/租户隔离、多图 processor 都会影响身份和可复用范围。

## 理解出口

学员能解释一个预测、指出一个假设、提出一条可以否证解释的观察。未达到时，把困难拆成更小例子，不重复整套讲义。

进度初始为 ready；根据真实对话填写 [progress](../progress.md)。本课远程实验仍是 designed，没有启动 GPU。
