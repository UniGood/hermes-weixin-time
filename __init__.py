from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Shanghai")
WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def get_period(hour: int) -> str:
    if hour < 6:
        return "凌晨"
    if hour < 8:
        return "早上"
    if hour < 12:
        return "上午"
    if hour < 14:
        return "中午"
    if hour < 18:
        return "下午"
    if hour < 20:
        return "傍晚"
    return "晚上"


def inject_time(platform: str = "", **kwargs):
    """Inject current time into every WeChat message."""
    if platform != "weixin":
        return None
    try:
        now = datetime.now(TZ)
        weekday = WEEKDAYS[now.weekday()]
        period = get_period(now.hour)
        short = f"{now.strftime('%H:%M')} {weekday} {period}"
        full = now.strftime("%Y-%m-%d %H:%M:%S")
        return {"context": f"[现在是 {short} | 精确时间: {full}]"}
    except Exception:
        return None


def register(ctx):
    ctx.register_hook("pre_llm_call", inject_time)
