# weixin-time 插件开发文档

## 概述

给微信消息注入当前准确时间，防止凯莉猜错时间（比如早上7点说"下午"）。

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

### 时间段划分

| 时段 | 时间范围 |
|------|---------|
| 凌晨 | 00:00 - 05:59 |
| 早上 | 06:00 - 07:59 |
| 上午 | 08:00 - 11:59 |
| 中午 | 12:00 - 13:59 |
| 下午 | 14:00 - 17:59 |
| 傍晚 | 18:00 - 19:59 |
| 晚上 | 20:00 - 23:59 |

### 注入格式

```
[现在是 07:40 周三 早上 | 精确时间: 2026-06-10 07:40:16]
```

### 覆盖范围

| 场景 | 是否注入 |
|------|---------|
| 微信私聊 | ✅ 注入 |
| 微信群聊 | ✅ 注入 |
| 飞书 | ❌ 不注入 |
| cron job | ❌ 不注入 |
| CLI 本地 | ❌ 不注入 |

### 与其他 hook 共存

与 active-message 插件的 hook 不冲突，会合并注入。active-message 先注册先调用，weixin-time 后注册后调用。

LLM 看到的效果：
```
用户消息

[active-message 的 context]
[weixin-time 的 context]
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
