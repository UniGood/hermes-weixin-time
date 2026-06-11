# hermes-weixin-time

Hermes Agent 微信时间注入插件 — 每条微信消息自动注入当前准确时间。

## 功能

通过 `pre_llm_call` hook，在每条微信消息触发 LLM 前，自动注入当前时间到 user message 里，让模型有准确的时间感知。

### 注入格式

```
[当前时间: 2026-06-10 14:30:25]
```

### 过滤条件

| 条件 | 说明 |
|------|------|
| platform == weixin | 仅微信消息注入 |
| user_message >= 3 字符 | 短消息（表情、"嗯"、"好"等）不注入 |

## 安装

### 方法一：手动安装

```bash
# 1. 创建插件目录
mkdir -p ~/.hermes/plugins/weixin-time/

# 2. 复制文件
cp plugin.yaml ~/.hermes/plugins/weixin-time/
cp __init__.py ~/.hermes/plugins/weixin-time/
cp DEVELOPMENT.md ~/.hermes/plugins/weixin-time/

# 3. 启用插件
hermes plugins enable weixin-time

# 4. 重启 gateway
hermes gateway restart
```

### 方法二：从 GitHub 克隆

```bash
# 1. 克隆仓库
cd /tmp && git clone https://github.com/UniGood/hermes-weixin-time.git

# 2. 复制到插件目录
cp -r hermes-weixin-time ~/.hermes/plugins/weixin-time/

# 3. 启用插件
hermes plugins enable weixin-time

# 4. 重启 gateway
hermes gateway restart
```

## 配置

无需额外配置，插件会自动检测微信平台并注入时间。

### 自定义

如果需要修改注入格式或过滤阈值，编辑 `~/.hermes/plugins/weixin-time/__init__.py`：

```python
# 修改时间格式
return {"context": f"[当前时间: {now.strftime('%H:%M')}]"}  # 只显示时分

# 修改最短注入阈值
_MIN_CHARS = 5  # 改为5个字符以上才注入
```

## 弃用方法

```bash
# 1. 禁用插件
hermes plugins disable weixin-time

# 2. 删除插件文件
rm -rf ~/.hermes/plugins/weixin-time/

# 3. 重启生效
hermes gateway restart
```

## 工作原理

```
用户发送微信消息
    ↓
pre_llm_call hook 触发
    ↓
检查 platform == weixin
    ↓
检查 user_message >= 3 字符
    ↓
注入 [当前时间: YYYY-MM-DD HH:MM:SS]
    ↓
LLM 看到带时间的完整消息
```

## 覆盖范围

| 场景 | 是否注入 |
|------|---------|
| 微信私聊（>=3字） | ✅ 注入 |
| 微信私聊（<3字） | ❌ 不注入 |
| 飞书 | ❌ 不注入 |
| cron job | ❌ 不注入 |
| CLI 本地 | ❌ 不注入 |

## 相关链接

- [Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs)
- [插件开发指南](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [Event Hooks 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks)
