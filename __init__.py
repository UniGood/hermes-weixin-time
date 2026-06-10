from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Shanghai")

# 最短注入阈值：消息字符数 < 此值时不注入时间
_MIN_CHARS = 3


def inject_time(platform: str = "", user_message: str = "", **kwargs):
    """Inject current time into short WeChat messages.

    Only injects when:
    - platform is weixin
    - user_message has >= _MIN_CHARS characters (skip reactions/typos)
    """
    if platform != "weixin":
        return None
    if len(user_message.strip()) < _MIN_CHARS:
        return None
    try:
        now = datetime.now(TZ)
        return {"context": f"[当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}]"}
    except Exception:
        return None


def register(ctx):
    ctx.register_hook("pre_llm_call", inject_time)
