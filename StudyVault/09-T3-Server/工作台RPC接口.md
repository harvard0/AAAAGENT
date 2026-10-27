---
module: t3-server
path: "t3-source/packages/contracts/src/rpc.ts"
keywords: [rpc, schema, commands]
updated: 2026-10-24
---

# 工作台RPC接口

#api-workbench #module-t3-server

## API 边界

T3 使用 `WsRpcGroup` 与共享 Schema 的类型化 RPC。核心依据：`t3-source/packages/contracts/src/rpc.ts`、`t3-source/packages/contracts/src/orchestration.ts`、`t3-source/apps/server/src/ws.ts`。调用常量来自 `ORCHESTRATION_WS_METHODS`；不要把桌面 JSON 行命令、管理 REST 和 T3 RPC 当成同一接口。

| 能力 | 合同/实现 | 结果含义 |
| --- | --- | --- |
| 派发命令 | `dispatchCommand` RPC → 规范化 → `OrchestrationEngine.dispatch` | 持久事件 sequence |
| 历史事件 | `OrchestrationEngine.readEvents` | 从排他游标后的有序历史；这是内部服务 API |
| 新领域事件 | `streamDomainEvents` / `subscribeDomainEvents` | 新事件热流；这是内部服务 API |
| 线程/快照/差异等查询 | `rpc.ts` 中逐项 Schema | 精确输入、输出与错误以合同为准 |

## Request / Response

以下是服务 API 的 TypeScript 形状，**不是可直接通过 HTTP POST 的 JSON 包装**：

```typescript
dispatch(command: OrchestrationCommand, options?: {
  origin?: OrchestrationClientOrigin
}): Effect<{ sequence: number }, OrchestrationDispatchError>
```

具体命令是带 type 的联合类型；新增或发送命令先查该分支 Schema。网络传输、鉴权、订阅生命周期由 `client-runtime/rpc` 和连接环境处理，调用方不手写猜测的 WebSocket 帧。

## 错误与恢复

| 场景 | 阅读位置 | 处理思路 |
| --- | --- | --- |
| 环境连接不可用 | `client-runtime/src/rpc/client.ts` | 核对环境身份与连接；不要盲目重复副作用命令 |
| 命令不合法或无法派发 | RPC 输入 Schema、OrchestrationDispatchError | 核对合同与实体状态 |
| 已接受但 Agent 失败 | ProviderCommandReactor、ProviderRuntimeIngestion | 继续读取领域事件与执行状态 |
| 响应丢失，结果不明 | 命令回执与 commandId | 用原命令身份核查，避免重复创建 |

## Related Notes

- [[T3服务端与事件编排]]
- [[T3客户端与共享状态]]
- [[T3共享合同与协议包]]
- [[工作执行与项目上下文]]
