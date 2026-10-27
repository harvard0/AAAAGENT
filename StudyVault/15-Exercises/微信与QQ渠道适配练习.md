---
module: exercises
path: "StudyVault/15-Exercises"
keywords: [practice, onboarding, channels]
updated: 2026-10-24
---

# 微信与QQ渠道适配练习

#practice #onboarding #module-channels

## Related Modules

- [[微信与QQ渠道适配]]
- [[请求流]]

每题先独立回答，再展开核对。路径简称均指本模块笔记 Key Files 中的项目相对路径。扩展题是设计练习，不表示功能已经实现。

## Exercise 1 — 代码阅读 [trace]

请分开画出微信私聊与 QQ 群摘要的处理路径。

> [!answer]- 查看答案
> 微信从 WeChatService 轮询到 WeChatTextConversation，进入私人聊天/工作；QQ 从原机器人成功发送后入 outbox，再提交社交 participations。QQ 摘要服务不是微信私人对话后端。

## Exercise 2 — 配置 [config]

QQ 适配器需要哪种社交凭据？

> [!answer]- 查看答案
> 只需要 channel 凭据与已绑定群配置。sync 是桌宠拉缓存用，admin 是管理策略用；不要为了方便共用三类 token。

## Exercise 3 — 调试 [debug]

社交服务重启后 QQ 出现重复回复，应该先确认什么？

> [!answer]- 查看答案
> 核对是否错误地同时走了通用生成/发送流程，以及 record_delivery 是否只在真实送达后触发。检查稳定事件 ID 与 outbox 去重；正常同步重试不应再次调用 QQ send。

## Exercise 4 — 扩展 [extend]

把一个新平台接到已有发送后的社交摘要链，最少需要保留哪些证据？

> [!answer]- 查看答案
> 稳定 role/group/actor/event 身份、实际用户文本、实际回复、平台送达回执与发生时间。持久化队列并对相同事件去重，拒绝把平台昵称当身份或用生成草稿当发送结果。

## Exercise 5 — 边界分析 [analysis]

仓库中的 QQ 桥接测试能证明真实群已经收到消息吗？

> [!answer]- 查看答案
> 不能。公开检查依赖现有迁移包，文档中的云端联调使用模拟 QQ 回执。平台自然新消息与实际送达回执仍需单独确认。

> [!summary]- 学习目标
> 能定位入口、解释数据归属、选择配置层、提出排查步骤，并为扩展保留现有边界。

## Related Notes

- [[微信与QQ渠道适配]]
- [[AAAAGENT学习地图]]
