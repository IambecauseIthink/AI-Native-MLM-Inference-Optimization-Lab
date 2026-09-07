# vllm-deep-dive

目标：建立源码地图。状态：planned。

Core 路径：固定 commit→一个请求的生命周期→scheduler/allocator/backend 分支→单变量补丁。

验收：用日志/trace 验证分支，测取消、异常、缓存和多请求隔离。每个阶段交付代码、正确性证据、实验合同和局限；Stretch 再扩展，不要求同时做四个项目。
