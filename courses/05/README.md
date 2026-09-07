# 05 · 相似提示词，为什么没有缓存收益？

**这次只解决：两个 prompt 语义非常相似，但第一行的时间戳不同。为什么可能没有 prefix cache 命中？**

用时 30–45 分钟，可随时暂停。让助手说“带我学第 05 课”，由助手先解释例子，再分步展开。无需先读完教材，不安装模型。

## 先理解这个例子

语义相似不等于 token 前缀相同。一个 block 的身份还依赖前面的 token，前缀早期改变会影响后续匹配。部分 block 不算完整命中；生成 logits 时仍需最后 token 重算。容量不足会驱逐块，开启缓存也不保证留下可重用前缀。

## 做一个预测，然后操作

block_size=8，把共同前缀从 8 改为 7，第二次请求还有一个完整 block 可复用吗？

允许回答“不确定，因为……”。在仓库根目录运行；每次只改变一个条件，恢复默认后再试下一个：

```bash
python3 scripts/lab.py lesson --id 05
python3 scripts/lab.py lesson --id 05 --set shared=7
python3 scripts/lab.py lesson --id 05 --set capacity=2
python3 scripts/lab.py lesson --id 05 --params
```

[交互图源码](../visuals/lesson-05.html) 可由助手直接在对话中展示；不要依赖 VS Code 默认 Markdown 预览执行脚本。可选本地预览方法见 [交互实验说明](../visuals/README.md)。结果始终标明 synthetic/analytical，不是 GPU 实测。

## 用一点原理解释

`首次目标请求可复用长度 ≤ floor(shared/block_size)×block_size；生成路径还受 floor((prompt_len−1)/block_size)×block_size 限制，并受保留块约束。`

一次 warm、高重复实验不能代表生产平均收益；应用层改模板、salt/租户隔离、多图 processor 都会影响身份和可复用范围。

## 带着问题看源码和教材

vLLM **v0.19.0 / 2a69949bdadf0e8942b7a1619b229cb475beef20**；源码导航不是运行证明。

- [KVCacheManager.get_computed_blocks](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/kv_cache_manager.py#L176) · `vllm/v1/core/kv_cache_manager.py` · L176。
- [BlockPool.get_cached_block](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/block_pool.py#L183) · `vllm/v1/core/block_pool.py` · L183。
- [BlockPool.cache_full_blocks](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/block_pool.py#L210) · `vllm/v1/core/block_pool.py` · L210。

get_computed_blocks 中核对 skip_reading_prefix_cache 与 prompt_length−1；再看 BlockPool.get_cached_block 的 group 标识和 cache_full_blocks 的完整块。toy 用完整前缀 tuple，不是实际 hash/引用计数算法。

教材：[MLSysBook · Caching](https://mlsysbook.ai/vol1/model_serving/model_serving.html)。在 Model Serving 搜索 caching，区分应用层响应缓存与 runtime prefix KV；vLLM 的精确匹配条件以本课固定源码为准。

## 今天如何结束

回答：为什么第三个完全重复的请求可能比第二个命中更多？为什么容量很小时又都不命中？

在 [进度记录](../progress.md) 留下自己的预测、观察、未知与下一步。读完或跑完不自动等于掌握，不自动进入下一课。

下一步：继续第 06 课：如果权重更小或激活低比特，究竟改变了哪些成本？

[远程验证设计](remote.md) · [教师页：带学时再看](teacher.md) · [回到课程入口](../README.md)
