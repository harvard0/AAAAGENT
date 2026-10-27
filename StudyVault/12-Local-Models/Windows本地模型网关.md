---
module: local-models
path: "windows/local-models"
keywords: [local-models, gateway, asr, capability]
updated: 2026-10-24
---

# Windows本地模型网关（重要度 ★★★）

#module-local-models #pattern-ports

## Purpose

为 Windows 可选的本地 ASR、TTS 和对话后端提供统一网关与显式能力路由。网关健康、权重就绪和真实模型效果分别验证。

## Key Files

| 项目相对路径 | 定位行 | 职责 |
| --- | --- | --- |
| `windows/local-models/src/cli.mjs` | 79 | 初始化、服务启动和 doctor 入口 |
| `windows/local-models/src/server.mjs` | 57 | 回环 HTTP、模型路由、并发与媒体请求 |
| `windows/local-models/src/config.mjs` | 13 | 协议、模型能力和路径校验 |
| `windows/local-models/package.json` | 1 | 服务、诊断及验证命令 |
| `windows/docs/LOCAL-LLM.md` | 1 | 历史真实对话效果与失败范围 |

## Public Interface

| 接口或入口 | 行为 |
| --- | --- |
| `GET /health / GET /v1/models` | 配置健康与已配置模型列表 |
| `POST /v1/chat/completions / /api/chat` | 按别名路由对话后端 |
| `POST /v1/audio/transcriptions / /v1/audio/speech` | ASR 与 TTS 适配 |
| `npm run configure / doctor / start` | 初始化、后端检查和启动 |

## Internal Flow

```text
桌宠所选本地能力 -> loopback 网关 -> 配置别名/能力选择
  +-> SenseVoice / Paraformer / Whisper 等 ASR
  +-> 已配置 TTS 或 Ollama 等后端
  -> 请求格式/并发/超时约束 -> 结果返回
其他未切换操作 ----------------> 原云端供应商
```

health 返回 configured 并提示运行 doctor 检查后端，不承诺模型已加载。请求检查 Host/Origin；活动请求达到 4 时返回 busy。原生 ASR 是按整段音频处理，不支持把它当作 partial-token 流。配置允许的远程后端须显式 allowRemote=true 且 HTTPS。文档记录的 4B 算术与复述失败、9B 未推理都是历史证据，本次未复跑。

## Dependencies

依赖按装配与数据交互描述；不把以下协作关系当作逐文件 import 图。

| 协作领域 | 进一步阅读 |
| --- | --- |
| 模型适配与媒体链路 | [[模型适配与媒体链路]] |
| 桌面宿主与平台边界 | [[桌面宿主与平台边界]] |

## Configuration

| 字段或环境 | 用途与限制 |
| --- | --- |
| `host / port / timeoutMs / maxBodyBytes` | 网关监听、超时与请求容量 |
| `provider.enabled / protocol / models` | 明确能力和模型别名，别名按能力去重 |
| `baseUrl / allowRemote / apiKeyEnv` | 后端端点与显式远程授权 |
| `numThreads / 模型文件字段` | 本地推理资源；配置校验不证明权重可用 |

## Testing

从项目根目录开启新的终端后执行：

```powershell
Set-Location windows/local-models
npm.cmd test
npm.cmd run doctor
```

网关合成测试与可用性诊断；doctor 需已配置后端，真实推理、样音和设备另外验。

命令为学习入口，本次建库未执行项目测试或真实服务调用。模块构建与平台要求见 [[构建测试与发布]]。

## Related Notes

- [[模型适配与媒体链路]]
- [[桌面宿主与平台边界]]
- [[Windows本地模型网关练习]]
- [[系统架构]]
- [[请求流]]
- [[数据流与来源]]
- [[来源与范围]]
