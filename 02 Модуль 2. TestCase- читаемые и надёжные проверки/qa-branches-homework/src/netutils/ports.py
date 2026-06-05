def parse_port(value):
    if isinstance(value, bool):
        raise TypeError("value must be int or str")
    if isinstance(value, int):
        if not (1 <= value <= 65535):
            raise ValueError("value out of range 1..65535")
        return value
    if isinstance(value, str):
        raw = value.strip()
        if not raw.isdigit():
            raise ValueError("value is not a valid integer string")
        port = int(raw)
        if not (1 <= port <= 65535):
            raise ValueError("value out of range 1..65535")
        return port
    raise TypeError("value must be int or str")