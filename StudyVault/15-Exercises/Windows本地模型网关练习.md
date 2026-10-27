---
module: exercises
path: "StudyVault/15-Exercises"
keywords: [practice, onboarding, local-models]
updated: 2026-10-24
---

# Windows本地模型网关练习

#practice #onboarding #module-local-models

## Related Modules

- [[Windows本地模型网关]]
- [[请求流]]

每题先独立回答，再展开核对。路径简称均指本模块笔记 Key Files 中的项目相对路径。扩展题是设计练习，不表示功能已经实现。

## Exercise 1 — 代码阅读 [trace]

一段 ASR multipart 音频从网关到本地识别器经过哪些选择？

> [!answer]- 查看答案
> createGateway 校验 Host/Origin、并发和 body，再按 /v1/audio/transcriptions 解析 formData，modelRoute 选择 asr 别名，按 provider.protocol 交给原生识别或后端适配。

## Exercise 2 — 配置 [config]

希望新增模型别名，需要核对哪些配置约束？

> [!answer]- 查看答案
> 检查 enabled、protocol 的能力支持和 models 中 alias/upstream 映射；同能力下别名不能重复。原生模型文件、线程及远程 HTTPS/allowRemote 另受校验。

## Exercise 3 — 调试 [debug]

health 返回 ok，但 ASR 仍失败，为什么？

> [!answer]- 查看答案
> health 只说明配置层存活。运行 doctor 并核对模型文件、后端服务、音频格式与能力别名；不要仅以 GET /health 推断权重加载和设备输入成功。

## Exercise 4 — 扩展 [extend]

添加一种本地 TTS，应该如何保持现有接口？

> [!answer]- 查看答案
> 在 config 注册协议及 tts 能力，在 providers 或专门适配器实现输入、音色、输出格式和取消，再由 server 路由接入。测试容量、并发、后端超时及返回音频。

## Exercise 5 — 边界分析 [analysis]

启用本地 ASR 是否意味着私人聊天完全离线？

> [!answer]- 查看答案
> 不意味着。dialogue、memory_turn、summary、perception、tts 可能仍是云端配置。逐项核对实际操作路由与请求日志，再判断数据流和费用。

> [!summary]- 学习目标
> 能定位入口、解释数据归属、选择配置层、提出排查步骤，并为扩展保留现有边界。

## Related Notes

- [[Windows本地模型网关]]
- [[AAAAGENT学习地图]]
