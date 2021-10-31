from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class UserBot:
    id: Optional[int] = None
    name: Optional[str] = None
    exchange: Optional[str] = "binance"
    key: Optional[str] = None
    secret: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'UserBot':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        exchange = from_union([from_str, from_none], obj.get("exchange"))
        key = from_union([from_str, from_none], obj.get("key"))
        secret = from_union([from_str, from_none], obj.get("secret"))
        return UserBot(id, name, exchange, key, secret)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["exchange"] = from_union([from_str, from_none], self.exchange)
        result["key"] = from_union([from_str, from_none], self.key)
        result["secret"] = from_union([from_str, from_none], self.secret)
        return result


def account_update_from_dict(s: Any) -> List[UserBot]:
    return from_list(UserBot.from_dict, s)


def account_update_to_dict(x: List[UserBot]) -> Any:
    return from_list(lambda x: to_class(UserBot, x), x)
