---
module: channels
path: "code/desktop-pet/wechat"
keywords: [wechat, qq, outbox, identity]
updated: 2026-10-24
---

# 微信与QQ渠道适配（重要度 ★★★）

#module-channels #pattern-idempotency

## Purpose

把外部聊天平台的消息和送达状态转换为应用能力，同时保留平台身份、会话和重试边界。微信私聊与 Windows QQ 群社交属于不同集成路径。

## Key Files

| 项目相对路径 | 定位行 | 职责 |
| --- | --- | --- |
| `code/desktop-pet/wechat/service.ts` | 29 | 登录、消息轮询与服务状态 |
| `code/desktop-pet/wechat/conversation.ts` | 64 | 微信文本对话及工作处理 |
| `windows/code/desktop-pet/tools/pet-cloud/qq-bridge/social_bridge.py` | 57 | 已发送回复的持久同步队列 |
| `windows/code/desktop-pet/tools/pet-cloud/qq-bridge/README.md` | 1 | 迁移包接线与平台回执要求 |
| `windows/docs/SOCIAL_MEMORY.md` | 1 | Windows 服务启停与验证范围 |

## Public Interface

| 接口或入口 | 行为 |
| --- | --- |
| `WeChatService` | 实现 WeChatManagement，管理登录与轮询 |
| `WeChatTextConversation` | 文本会话入口，结合工作状态与输出适配 |
| `record_delivery(item, reply, reply_id)` | 仅在 QQ 实际发送并保存 replied 后入队 |
| `Windows participations` | 向社交服务提交实际发言、回复和回执 |

## Internal Flow

```text
微信登录/轮询 -> 平台消息 -> 文本会话 -> 私人聊天或工作
QQ 现有 Runtime -> gateway.send -> 平台回复 ID -> replied
  -> record_delivery -> social-outbox -> participations
  -> 摘要缓存 (不会触发第二次 QQ 发送)
```

昵称只用于显示，身份依赖稳定的群、成员和事件标识；QQ 标识在进入社交服务前做确定性散列。仓库只含 QQ 适配器及接线补丁，不含完整迁移包或账号。适配器请求超时可重试同一事件；它本身不再向 QQ 发送回复。仅上传图片、发送失败或结果不明均不能伪造送达回执。微信登录和真实平台投递需要独立账号验证。

## Dependencies

依赖按装配与数据交互描述；不把以下协作关系当作逐文件 import 图。

| 协作领域 | 进一步阅读 |
| --- | --- |
| 运行时与对话编排 | [[运行时与对话编排]] |
| 模型适配与媒体链路 | [[模型适配与媒体链路]] |
| 管理服务与配置 | [[管理服务与配置]] |
| 角色社交服务与缓存 | [[角色社交服务与缓存]] |
| 工作执行与项目上下文 | [[工作执行与项目上下文]] |

## Configuration

| 字段或环境 | 用途与限制 |
| --- | --- |
| `微信登录/运行状态` | 由 WeChatService 与管理能力持有，不把账号状态放入源码 |
| `social-channel.json` | 迁移包侧 channel 凭据及绑定群；不是 admin 凭据 |
| `social-outbox.sqlite` | QQ 待同步事件持久队列，重启后继续 |
| `Windows SID ACL` | 现有文档要求保护本机配置与数据库 |

## Testing

从项目根目录开启新的终端后执行：

```powershell
Set-Location code/desktop-pet
npm.cmd run build
node --test dist/tests/wechat/conversation.test.js
```

微信会话的合成测试；QQ check_social_bridge.py 依赖未随仓库提供的迁移包，不能在此直接当作独立测试运行。

命令为学习入口，本次建库未执行项目测试或真实服务调用。模块构建与平台要求见 [[构建测试与发布]]。

## Related Notes

- [[运行时与对话编排]]
- [[模型适配与媒体链路]]
- [[管理服务与配置]]
- [[角色社交服务与缓存]]
- [[工作执行与项目上下文]]
- [[微信与QQ渠道适配练习]]
- [[系统架构]]
- [[请求流]]
- [[数据流与来源]]
- [[来源与范围]]
