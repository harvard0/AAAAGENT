---
module: dashboard
path: "."
keywords: [moc, onboarding, aaaagent]
updated: 2026-10-24
---

# AAAAGENT学习地图

#dashboard #onboarding

## Architecture Overview

模式：本机端口编排 + 独立社交服务 + T3 事件驱动工程工作台。技术栈：TypeScript/Node、SQLite、React/Effect、Swift/WebKit 与 Electron。源码基线和抽样边界见 [[来源与范围]]。

- [[系统架构]]
- [[请求流]]
- [[数据流与来源]]

## Module Map

| 领域 | 用途 | 核心入口 | 笔记与练习 |
| --- | --- | --- | --- |
| 运行时与对话编排 | 把桌面命令转换成有作用域的对话轮次，协调输入、聊天或工作分流、持久化和输出 | `code/desktop-pet` | [[运行时与对话编排]] · [[运行时与对话编排练习]] |
| 私人记忆与上下文 | 持久化私人对话、长期记忆与来源，并在预算内选择允许进入本轮模型请求的上下文 | `code/desktop-pet/memory` | [[私人记忆与上下文]] · [[私人记忆与上下文练习]] |
| 模型适配与媒体链路 | 将稳定的对话、感知和 TTS 能力映射到供应商请求，并处理媒体捕获、播放、计费授权与完整请求预算 | `code/desktop-pet/providers` | [[模型适配与媒体链路]] · [[模型适配与媒体链路练习]] |
| 角色社交服务与缓存 | 在独立数据库中维护角色的群聊参与经历，并向私人桌宠提供经过授权的只读摘要缓存 | `code/desktop-pet/companion/cloud` | [[角色社交服务与缓存]] · [[角色社交服务与缓存练习]] |
| 工作执行与项目上下文 | 把工作意图转为可确认任务，再关联项目、执行器和回执 | `code/desktop-pet/harness` | [[工作执行与项目上下文]] · [[工作执行与项目上下文练习]] |
| 管理服务与配置 | 提供本机管理 UI 与受控 HTTP 操作，统一查看和修改记忆、模型、项目、任务及表现设置 | `code/desktop-pet/management` | [[管理服务与配置]] · [[管理服务与配置练习]] |
| 微信与QQ渠道适配 | 把外部聊天平台的消息和送达状态转换为应用能力，同时保留平台身份、会话和重试边界 | `code/desktop-pet/wechat` | [[微信与QQ渠道适配]] · [[微信与QQ渠道适配练习]] |
| T3服务端与事件编排 | 承载工作台类型化 RPC、命令编排、事件存储与投影，并通过供应商适配器驱动实际 Agent 会话 | `t3-source/apps/server` | [[T3服务端与事件编排]] · [[T3服务端与事件编排练习]] |
| T3客户端与共享状态 | 呈现工作台线程、项目、终端和结果，并通过共享 client-runtime 连接环境、调用 RPC 和消费领域状态 | `t3-source/apps/web` | [[T3客户端与共享状态]] · [[T3客户端与共享状态练习]] |
| 桌面宿主与平台边界 | 提供窗口、渲染、设备与进程桥接，连接桌宠界面和可信 Node 后端 | `code/desktop-pet/desktop` | [[桌面宿主与平台边界]] · [[桌面宿主与平台边界练习]] |
| Windows本地模型网关 | 为 Windows 可选的本地 ASR、TTS 和对话后端提供统一网关与显式能力路由 | `windows/local-models` | [[Windows本地模型网关]] · [[Windows本地模型网关练习]] |
| T3共享合同与协议包 | 在服务端和各客户端间共享 Schema、协议、平台抽象及通用工具，避免各端独立猜测消息格式 | `t3-source/packages` | [[T3共享合同与协议包]] · [[T3共享合同与协议包练习]] |


## API Surface

| 接口 | 入口 | 说明 |
| --- | --- | --- |
| 本机管理 HTTP | `/api/snapshot`、`/api/settings` 等 | [[管理HTTP接口]] |
| 角色社交 HTTP | `/v1/{roleId}/events`、sync、deliveries；Windows participations | [[社交HTTP接口]] |
| 工作台 RPC | ORCHESTRATION_WS_METHODS / WsRpcGroup | [[工作台RPC接口]] |
| 桌宠桥接 | command/event 的 JSON 行与宿主 IPC | [[桌面宿主与平台边界]] |
| 可选本地模型 | health、models、chat、audio | [[Windows本地模型网关]] |

## Getting Started

按 [[快速上手]] 从当前平台预览开始，再按 [[命令与排查速查]] 定向阅读与测试。根目录没有统一 npm 工程，各子项目独立安装。真实服务配置、引擎和素材要求见 [[环境配置与验证边界]] 与 [[构建测试与发布]]。

## Tag Index

完整批准的注册表和层次规则见 [[标签标准]]。只使用已注册的英文小写 kebab-case；module 与 api/pattern 细节共同标注，practice 表示折叠答案练习。

| 注册标签 | 含义 |
| --- | --- |
| `#dashboard` | 导航入口 |
| `#onboarding` | 上手学习 |
| `#quick-reference` | 命令速查 |
| `#practice` | 折叠答案练习 |
| `#arch-system` | 系统边界 |
| `#arch-request-flow` | 请求链路 |
| `#arch-data-flow` | 持久化与来源 |
| `#module-runtime` | 运行时 |
| `#module-memory` | 私人记忆 |
| `#module-model-media` | 模型与媒体 |
| `#module-social` | 角色社交 |
| `#module-workbench` | 工作执行 |
| `#module-management` | 管理页 |
| `#module-channels` | 消息渠道 |
| `#module-t3-server` | T3 服务端 |
| `#module-t3-client` | T3 客户端 |
| `#module-desktop` | 桌面宿主 |
| `#module-local-models` | 本地模型 |
| `#module-t3-packages` | T3 共享包 |
| `#pattern-ports` | 能力接口与装配 |
| `#pattern-background-jobs` | 后台任务 |
| `#pattern-provenance` | 来源与版本 |
| `#pattern-idempotency` | 去重及未知结果 |
| `#pattern-rpc` | 类型化远程调用 |
| `#pattern-event-stream` | 事件与投影 |
| `#config-environment` | 环境配置 |
| `#test-validation` | 检查及证据 |
| `#api-management` | 管理 HTTP |
| `#api-social` | 社交 HTTP |
| `#api-workbench` | 工作台 RPC |

## Onboarding Path

1. [[系统架构]] → [[请求流]] → [[数据流与来源]]：先解释边界。
2. [[运行时与对话编排]] → [[私人记忆与上下文]] → [[模型适配与媒体链路]]：追踪一轮私人对话。
3. [[角色社交服务与缓存]] → [[微信与QQ渠道适配]]：区分真实参与和缓存引用。
4. [[工作执行与项目上下文]] → [[T3服务端与事件编排]] → [[T3客户端与共享状态]] → [[T3共享合同与协议包]]：追踪一项工程任务。
5. [[管理服务与配置]] → [[桌面宿主与平台边界]] → [[Windows本地模型网关]]：理解平台与操作入口。
6. 完成各模块对应练习，遇到错误回到 Key Files 核对证据。

## 学习与维护工具

- [[构建测试与发布]]
- [[环境配置与验证边界]]
- [[来源与范围]]
- [[建库自检]]
- [[README|StudyVault使用说明]]

## 范围政策

按 12 个主要领域建立入门地图；不是逐文件说明。T3 的辅助子系统归入服务端、客户端和共享包笔记。完整 QQ 迁移包、私人资源和运行数据没有纳入；移动端源码、原生设备、远程连接与模型效果不作已验收承诺。用户已批准该划分和标签表。

## Related Notes

- [[快速上手]]
- [[来源与范围]]
- [[建库自检]]
