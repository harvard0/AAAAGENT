---
module: social
path: "code/desktop-pet/companion/cloud/server.ts"
keywords: [api, social, receipts]
updated: 2026-10-24
---

# 社交HTTP接口

#api-social #module-social

## Endpoints

除 `/health` 外，以下相对路径均带 `/v1/{roleId}/` 前缀。来源是根目录与 Windows 各自的 `companion/cloud/server.ts` 以及 `docs/SOCIAL_PROTOCOL.md`。

| 方法 | 路径 | 凭据 | 作用 |
| --- | --- | --- | --- |
| GET | `/health` | 无 | `{ok:true,protocol:1}` 存活检查 |
| POST | `events` | channel | 通用群事件，返回 202 |
| POST | `deliveries/claim` | channel | 返回 delivery 或无待发项 |
| POST | `deliveries/ack` | channel | 提交真实平台回执 |
| POST | `deliveries/fail` | channel | 明确未发送或结果不明 |
| POST | `participations` | channel | **Windows 扩展**，记录已送达回复 |
| GET | `sync?after=N` | sync | epoch、cursor、授权组与 upsert/delete |
| GET | `status`、`jobs` | admin | 无正文的状态与异常 |
| PUT | `group`、`persona` | admin | expectedRevision 比较更新 |
| DELETE | `experiences/{id}` | admin | 遗忘并传播派生撤回 |
| POST | `jobs/resolve` | admin | 核查未知或失败事件 |

## Request / Response

通用 ACK 请求只说明真实发送已完成；示例标识是合成占位值：

```json
{"deliveryId":"delivery-example","lease":"lease-from-claim","receipt":"platform-receipt"}
```

成功：

```json
{"ok":true}
```

错误形状来自服务端捕获分支：

```json
{"error":"unauthorized"}
```

| 状态 | 条件示例 |
| --- | --- |
| 401 | 缺失或不匹配的 Bearer 凭据 |
| 403 | 凭据角色不符，或携带浏览器 Origin |
| 404 | 路由/角色路径不匹配 |
| 409 | 同事件 ID 异正文、版本冲突或身份变化等业务冲突 |
| 500 | 未识别内部异常，不输出正文 |

请求字段以 `protocol.ts` 和平台实现为准，额外字段拒绝。不要把 ACK 示例当作可随意伪造的平台回执。

## Related Notes

- [[角色社交服务与缓存]]
- [[微信与QQ渠道适配]]
- [[请求流]]
- [[数据流与来源]]
