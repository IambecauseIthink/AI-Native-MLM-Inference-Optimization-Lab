# 02 · GPU 带宽已满，还能提速吗？

**这次只解决：你最初判断“并发 1 已经拉满，增加并发可能无收益”。现在只讨论权重读取带宽：它满了还可能有收益吗？**

用时 30–45 分钟，可随时暂停。让助手说“带我学第 02 课”，由助手先解释例子，再分步展开。无需先读完教材，不安装模型。

## 先理解这个例子

把 X[B,K] 看成 B 行请求，把 W[K,N] 看成同一层权重，X@W 得到 [B,N]。这就是 PyTorch 中 matmul 的 shape 关系；这里不安装 PyTorch，也不运行模型。B 增大时，W 的元素数没有变，计算量增加；同一份权重可服务更多行。

## 做一个预测，然后操作

只把 batch 从 8 改成 128，权重总字节是否改变？单步更慢和总行吞吐更高能同时发生吗？

允许回答“不确定，因为……”。在仓库根目录运行；每次只改变一个条件，恢复默认后再试下一个：

```bash
python3 scripts/lab.py lesson --id 02
python3 scripts/lab.py lesson --id 02 --set batch=128
python3 scripts/lab.py lesson --id 02 --set batch=128 --set compute_tflops=10
python3 scripts/lab.py lesson --id 02 --params
```

[交互图源码](../visuals/lesson-02.html) 可由助手直接在对话中展示；不要依赖 VS Code 默认 Markdown 预览执行脚本。可选本地预览方法见 [交互实验说明](../visuals/README.md)。结果始终标明 synthetic/analytical，不是 GPU 实测。

## 用一点原理解释

`FLOPs = 2BKN；bytes = KN·weight_bytes + 2B(K+N)；I=FLOPs/bytes；单步时间下界=max(FLOPs/算力, bytes/带宽)。`

显存带宽饱和不代表每个输出已分摊最少字节；计算上限、KV 或 launch 又可能成为新瓶颈。

## 带着问题看源码和教材

vLLM **v0.19.0 / 2a69949bdadf0e8942b7a1619b229cb475beef20**；源码导航不是运行证明。

- [GPUModelRunner.execute_model](https://github.com/vllm-project/vllm/blob/2a69949bdadf0e8942b7a1619b229cb475beef20/vllm/v1/worker/gpu_model_runner.py#L3770) · `vllm/v1/worker/gpu_model_runner.py` · L3770。

在 execute_model 中找 scheduler_output、输入准备与 model forward。先理解输入如何成为一批，再探索 kernel；不要把这个入口存在视为该部署确实选择了这条 runner 分支。

教材：[MLSysBook · Roofline Model](https://mlsysbook.ai/vol1/hw_acceleration/hw_acceleration.html)。只读 Roofline Model 的定义和算术强度公式；带着“每生成一个 token 分摊多少权重字节”阅读。

## 今天如何结束

回答：如果 profile 显示实际时间远大于这个理论下界，还可能少算了什么？

在 [进度记录](../progress.md) 留下自己的预测、观察、未知与下一步。读完或跑完不自动等于掌握，不自动进入下一课。

下一步：继续第 03 课，加入本课没有计算的 KV 容量。

[远程验证设计](remote.md) · [教师页：带学时再看](teacher.md) · [回到课程入口](../README.md)
