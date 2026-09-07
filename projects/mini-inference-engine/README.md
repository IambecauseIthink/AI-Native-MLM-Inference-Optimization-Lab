# mini-inference-engine

目标：理解执行依赖。状态：planned。

Core 路径：CPU 解析模型与调度模拟器（明确 synthetic）→KV block allocator 教学实现→小模型 correctness oracle。

验收：实现真实 token 生成需远程环境；比较 eager/cache 路径；教学引擎不能冒充生产 baseline。每个阶段交付代码、正确性证据、实验合同和局限；Stretch 再扩展，不要求同时做四个项目。
