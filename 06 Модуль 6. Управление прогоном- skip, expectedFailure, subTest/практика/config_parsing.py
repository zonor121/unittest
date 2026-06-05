from __future__ import annotations


def parse_port(value: str) -> int:
    if not isinstance(value, str):
        raise TypeError("port value must be str")
    
    raw = value.strip()
    if not raw.isdigit():
        raise ValueError(f"port is not a valid decimal integer: {value!r}")
    
    port = int(raw)
    if not (1 <= port <= 65535):
        raise ValueError(f"port out of range 1..65535: {value!r}")
    
    return port


def parse_bool(value: str) -> bool:
    if not isinstance(value, str):
        raise TypeError("bool value must be str")
    
    token = value.strip().lower()
    if token in {"1", "true", "yes", "on"}:
        return True
    if token in {"0", "false", "no", "off"}:
        return False
    
    raise ValueError(f"invalid boolean literal: {value!r}")


def parse_csv(value: str) -> list[str]:
    if not isinstance(value, str):
        raise TypeError("csv value must be str")
    
    return [item.strip() for item in value.split(",") if item.strip()]