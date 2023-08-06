from typing import Optional

def parse_int(s: str) -> Optional[int]:
    if type(s) is not int and type(s) is not str:
        return None
    try:
        return int(s)
    except ValueError:
        return None

def parse_float(s: str) -> Optional[float]:
    if type(s) is not float and type(s) is not str:
        return None
    try:
        return float(s)
    except ValueError:
        return None

def parse_bool(s: str) -> Optional[bool]:
    if type(s) is not bool and type(s) is not str:
        return None
    if len(s) == 0:
        return None
    if s == "0" or s.lower() == "false":
        return False
    return True
