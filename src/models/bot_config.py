from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast

T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Long:
    enabled: Optional[bool] = None
    iprc_m_ar_coeffs: Optional[List[List[float]]] = None
    iprc_const: Optional[float] = None
    iqty_m_ar_coeffs: Optional[List[List[float]]] = None
    iqty_const: Optional[float] = None
    markup_m_ar_coeffs: Optional[List[List[float]]] = None
    markup_const: Optional[float] = None
    pbr_limit: Optional[float] = None
    pbr_stop_loss: Optional[float] = None
    rprc_m_ar_coeffs: Optional[List[List[float]]] = None
    rprc_p_br_coeffs: Optional[List[List[float]]] = None
    rprc_const: Optional[float] = None
    rqty_m_ar_coeffs: Optional[List[List[float]]] = None
    rqty_const: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Long':
        assert isinstance(obj, dict)
        enabled = from_union([from_bool, from_none], obj.get("enabled"))
        iprc_m_ar_coeffs = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none],
                                      obj.get("iprc_MAr_coeffs"))
        iprc_const = from_union([from_float, from_none], obj.get("iprc_const"))
        iqty_m_ar_coeffs = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none],
                                      obj.get("iqty_MAr_coeffs"))
        iqty_const = from_union([from_float, from_none], obj.get("iqty_const"))
        markup_m_ar_coeffs = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none],
                                        obj.get("markup_MAr_coeffs"))
        markup_const = from_union([from_float, from_none], obj.get("markup_const"))
        pbr_limit = from_union([from_float, from_none], obj.get("pbr_limit"))
        pbr_stop_loss = from_union([from_float, from_none], obj.get("pbr_stop_loss"))
        rprc_m_ar_coeffs = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none],
                                      obj.get("rprc_MAr_coeffs"))
        rprc_p_br_coeffs = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none],
                                      obj.get("rprc_PBr_coeffs"))
        rprc_const = from_union([from_float, from_none], obj.get("rprc_const"))
        rqty_m_ar_coeffs = from_union([lambda x: from_list(lambda x: from_list(from_float, x), x), from_none],
                                      obj.get("rqty_MAr_coeffs"))
        rqty_const = from_union([from_float, from_none], obj.get("rqty_const"))
        return Long(enabled, iprc_m_ar_coeffs, iprc_const, iqty_m_ar_coeffs, iqty_const, markup_m_ar_coeffs,
                    markup_const, pbr_limit, pbr_stop_loss, rprc_m_ar_coeffs, rprc_p_br_coeffs, rprc_const,
                    rqty_m_ar_coeffs, rqty_const)

    def to_dict(self) -> dict:
        result: dict = {}
        result["enabled"] = from_union([from_bool, from_none], self.enabled)
        result["iprc_MAr_coeffs"] = from_union([lambda x: from_list(lambda x: from_list(to_float, x), x), from_none],
                                               self.iprc_m_ar_coeffs)
        result["iprc_const"] = from_union([to_float, from_none], self.iprc_const)
        result["iqty_MAr_coeffs"] = from_union([lambda x: from_list(lambda x: from_list(to_float, x), x), from_none],
                                               self.iqty_m_ar_coeffs)
        result["iqty_const"] = from_union([to_float, from_none], self.iqty_const)
        result["markup_MAr_coeffs"] = from_union([lambda x: from_list(lambda x: from_list(to_float, x), x), from_none],
                                                 self.markup_m_ar_coeffs)
        result["markup_const"] = from_union([to_float, from_none], self.markup_const)
        result["pbr_limit"] = from_union([to_float, from_none], self.pbr_limit)
        result["pbr_stop_loss"] = from_union([to_float, from_none], self.pbr_stop_loss)
        result["rprc_MAr_coeffs"] = from_union([lambda x: from_list(lambda x: from_list(to_float, x), x), from_none],
                                               self.rprc_m_ar_coeffs)
        result["rprc_PBr_coeffs"] = from_union([lambda x: from_list(lambda x: from_list(to_float, x), x), from_none],
                                               self.rprc_p_br_coeffs)
        result["rprc_const"] = from_union([to_float, from_none], self.rprc_const)
        result["rqty_MAr_coeffs"] = from_union([lambda x: from_list(lambda x: from_list(to_float, x), x), from_none],
                                               self.rqty_m_ar_coeffs)
        result["rqty_const"] = from_union([to_float, from_none], self.rqty_const)
        return result


@dataclass
class BotConfig:
    config_name: Optional[str] = None
    logging_level: Optional[int] = None
    long: Optional[Long] = None
    max_span: Optional[float] = None
    min_span: Optional[float] = None
    n_spans: Optional[int] = None
    shrt: Optional[Long] = None

    @staticmethod
    def from_dict(obj: Any) -> 'BotConfig':
        assert isinstance(obj, dict)
        config_name = from_union([from_str, from_none], obj.get("config_name"))
        logging_level = from_union([from_int, from_none], obj.get("logging_level"))
        long = from_union([Long.from_dict, from_none], obj.get("long"))
        max_span = from_union([from_float, from_none], obj.get("max_span"))
        min_span = from_union([from_float, from_none], obj.get("min_span"))
        n_spans = from_union([from_int, from_none], obj.get("n_spans"))
        shrt = from_union([Long.from_dict, from_none], obj.get("shrt"))
        return BotConfig(config_name, logging_level, long, max_span, min_span, n_spans, shrt)

    def to_dict(self) -> dict:
        result: dict = {}
        result["config_name"] = from_union([from_str, from_none], self.config_name)
        result["logging_level"] = from_union([from_int, from_none], self.logging_level)
        result["long"] = from_union([lambda x: to_class(Long, x), from_none], self.long)
        result["max_span"] = from_union([to_float, from_none], self.max_span)
        result["min_span"] = from_union([to_float, from_none], self.min_span)
        result["n_spans"] = from_union([from_int, from_none], self.n_spans)
        result["shrt"] = from_union([lambda x: to_class(Long, x), from_none], self.shrt)
        return result


def bot_config_from_dict(s: Any) -> BotConfig:
    return BotConfig.from_dict(s)


def bot_config_to_dict(x: BotConfig) -> Any:
    return to_class(BotConfig, x)
