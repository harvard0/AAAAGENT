---
module: management
path: "code/desktop-pet/management/server.ts"
keywords: [api, management, revision]
updated: 2026-10-24
---

# 管理HTTP接口

#api-management #module-management

## Endpoints

服务动态监听回环端口，API 使用 Bearer，写入同时校验当前 Origin。以下选取核心入口，并非完整客户端 SDK 合同；更多领域路由在 `management/server.ts` 分派。

| 方法 | 路径 | 行为 |
| --- | --- | --- |
| GET | `/api/snapshot` | 当前管理快照 |
| GET | `/api/records` | 指定 kind/state 的分页记录 |
| GET | `/api/context` | 当前角色和 query 的上下文预览 |
| GET / PUT | `/api/prompt` | 查看或修改角色提示词 |
| POST | `/api/records/edit` | 带操作标识、原因和版本的受控编辑 |
| PUT | `/api/settings` | 保存设置及 expectedRevision |
| POST | `/api/settings/rollback` | 按当前与目标版本回退参数 |
| GET | `/api/memory-pending` | 未完成记忆请求状态 |
| POST | `/api/memory-pending/retry`、`/cancel` | 重试或取消指定未完成请求 |

## Request / Response

`PUT /api/settings` 的请求外层如下；settings 应为该版本合同定义的完整有效对象，不能把示意省略字段直接提交：

```typescript
// ManagedSettings 定义：code/desktop-pet/contracts/management.ts
type SaveSettingsRequest = {
  expectedRevision: number;
  settings: ManagedSettings;
};
```

ManagedSettings 定义位于 `code/desktop-pet/contracts/management.ts`；上方仅展示类型关系。成功返回 SettingsSnapshot，包含 revision、effectiveRevision、saved、effective、pending 和 applyOn: restart。保存不是即时热更新。避免在入门笔记复制易漂移的完整配置对象。

错误响应统一形状：

```json
{"error":{"code":"version_conflict","message":"..."}}
```

| 状态 | code |
| --- | --- |
| 400 | invalid_request |
| 401 | unauthorized |
| 403 | forbidden |
| 404 | not_found |
| 409 | version_conflict |
| 503 | unavailable |
| 500 | internal_error |

setup 模式可能拒绝运行期操作。浏览器外观接缝不提供绕过 API 权限的途径。

## Related Notes

- [[管理服务与配置]]
- [[私人记忆与上下文]]
- [[工作执行与项目上下文]]
