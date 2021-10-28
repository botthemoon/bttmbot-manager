from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Bot:
    config_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Bot':
        assert isinstance(obj, dict)
        config_id = from_union([from_int, from_none], obj.get("config_id"))
        user_id = from_union([from_int, from_none], obj.get("user_id"))
        status = from_union([from_str, from_none], obj.get("status"))
        return Bot(config_id, user_id, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["config_id"] = from_union([from_int, from_none], self.config_id)
        result["user_id"] = from_union([from_int, from_none], self.user_id)
        result["status"] = from_union([from_str, from_none], self.status)
        return result


def bot_from_dict(s: Any) -> Bot:
    return Bot.from_dict(s)
