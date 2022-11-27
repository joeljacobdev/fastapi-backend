from typing import Any
from orjson import loads as _loads, dumps as _dumps


def loads(json: str | bytes) -> Any:
    print('custom loads')
    return _loads(json)


def dumps(obj: Any, **kwargs) -> str:
    return dumps_bytes(obj, **kwargs).decode(encoding='utf-8')


def dumps_bytes(obj: Any, **kwargs) -> bytes:
    # bytes are encoded in utf-8
    return _dumps(obj, **kwargs)
