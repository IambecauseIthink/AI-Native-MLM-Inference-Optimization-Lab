# 03 · 权重放得下，为什么还 OOM？

**这次只解决：假设 GPU 容量 64 GiB、权重 54 GiB、其他开销 6 GiB，剩下 4 GiB。请求变长后为何可能装不下？**

用时 30–45 分钟，可随时暂停。让助手说“带我学第 03 课”，由助手先解释例子，再分步展开。无需先读完教材，不安装模型。

## 先理解这个例子

K 和 V 各存一份。对每层、每请求、每 token，需要 Hkv×D 个元素，而不是 Hq×D。GQA 的 query heads 多于 KV heads，因此 KV 可以更小。分页按整块分配，最后一块的空槽仍占空间。

## 做一个预测，然后操作

只把 tokens 从 1025 改成 8193，模型权重不变，总容量会不会越过假定的 64 GiB？

允许回答“不确定，因为……”。在仓库根目录运行；每次只改变一个条件，恢复默认后再试下一个：

```bash
python3 scripts/lab.py lesson --id 03
python3 scripts/lab.py lesson --id 03 --set tokens=8193
python3 scripts/lab.py lesson --id 03 --set tokens=8193 --set kv_bytes=1
python3 scripts/lab.py lesson --id 03 --params
```

[交互图源码](../visuals/lesson-03.html) 可由助手直接在对话中展示；不要依赖 VS Code 默认 Markdown 预览执行脚本。可选本地预览方法见 [交互实验说明](../visuals/README.md)。结果始终标明 synthetic/analytical，不是 GPU 实测。

## 用一点原理解释

`raw KV = 2×L×Hkv×D×bytes×Σtokens；分页 KV 对每个请求把 tokens 向上取整到 block_size 后再求和。`

更多容量不等于更高每步效率；FP8 scale、转换成本、真实 allocator 与工作区会改变效果。

## 带着问题看源码和教材

vLLM **v0.19.0 / 2a69949bdadf0e8942b7a1619b229cb475beef20**；源码导航不是运行证明。

- [KVCacheManager.allocate_slots](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/core/kv_cache_manager.py#L257) · `vllm/v1/core/kv_cache_manager.py` · L257。

打开 allocate_slots，找需要的 token 数、可用 blocks 与分配失败路径。补看函数周围的 coordinator；模型不同会有不同 KV group，不能简单除以 TP。

教材：[MLSysBook · Memory](https://mlsysbook.ai/vol1/hw_acceleration/hw_acceleration.html)。在硬件章节搜索 Memory，区分 memory capacity 和 bandwidth；缓存公式使用本课推导，不能把教材的通用内存图当某型号实测。

## 今天如何结束

回答：把 KV bytes 从 2 改为 1 后，能否立刻声称业务质量不变、QPS 翻倍？

在 [进度记录](../progress.md) 留下自己的预测、观察、未知与下一步。读完或跑完不自动等于掌握，不自动进入下一课。

下一步：继续第 04 课，看容量和 token 预算如何约束调度。

[远程验证设计](remote.md) · [教师页：带学时再看](teacher.md) · [回到课程入口](../README.md)
