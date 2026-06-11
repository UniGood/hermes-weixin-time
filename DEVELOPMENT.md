# weixin-time 插件开发文档

## 概述

给微信消息注入当前时间，让模型有准确的时间感知。

## 创建时间

2026-06-10

## 文件清单

| 操作 | 文件 | 说明 |
|------|------|------|
| 新建 | `~/.hermes/plugins/weixin-time/plugin.yaml` | 插件元信息 |
| 新建 | `~/.hermes/plugins/weixin-time/__init__.py` | 核心逻辑 |
| 新建 | `~/.hermes/plugins/weixin-time/DEVELOPMENT.md` | 本文档 |
| 启用 | `hermes plugins enable weixin-time` | 激活插件 |
| 重启 | `hermes gateway restart` | 加载新插件 |

## 工作原理

通过 `pre_llm_call` hook，在每条微信消息触发 LLM 前，自动注入当前时间到 user message 里。

### 注入格式

```
[当前时间: 2026-06-10 14:30:25]
```

### 过滤条件

| 条件 | 说明 |
|------|------|
| platform == weixin | 仅微信消息注入 |
| user_message >= 3 字符 | 短消息（表情、"嗯"、"好"等）不注入 |

### 覆盖范围

| 场景 | 是否注入 |
|------|---------|
| 微信私聊（>=3字） | ✅ 注入 |
| 微信私聊（<3字） | ❌ 不注入 |
| 飞书 | ❌ 不注入 |
| cron job | ❌ 不注入 |
| CLI 本地 | ❌ 不注入 |

### 与其他 hook 共存

与其他 `pre_llm_call` 插件的 hook 不冲突，会按注册顺序合并注入。

LLM 看到的效果：
```
用户消息

[其他插件的 context]
[当前时间: 2026-06-10 14:30:25]
```

## 弃用方法

### 第一步：禁用插件

```bash
hermes plugins disable weixin-time
```

### 第二步：删除插件文件

```bash
rm -rf ~/.hermes/plugins/weixin-time/
```

### 第三步：重启生效

```bash
hermes gateway restart
```
