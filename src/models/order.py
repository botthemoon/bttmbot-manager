from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast

from src.services.logger import logger

T = TypeVar("T")


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except Exception as ex:
            logger.debug("Order assert exception: " + str(fs) + str(x))
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Order:
    client_order_id: Optional[str] = None
    cum_qty: Optional[str] = None
    cum_quote: Optional[str] = None
    executed_qty: Optional[str] = None
    order_id: Optional[int] = None
    avg_price: Optional[str] = None
    orig_qty: Optional[str] = None
    price: Optional[str] = None
    reduce_only: Optional[bool] = None
    side: Optional[str] = None
    position_side: Optional[str] = None
    status: Optional[str] = None
    stop_price: Optional[str] = None
    close_position: Optional[bool] = None
    symbol: Optional[str] = None
    time_in_force: Optional[str] = None
    order_type: Optional[str] = None
    orig_type: Optional[str] = None
    activate_price: Optional[str] = None
    price_rate: Optional[str] = None
    update_time: Optional[int] = None
    working_type: Optional[str] = None
    price_protect: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Order':
        assert isinstance(obj, dict)
        client_order_id = from_union([from_str, from_none], obj.get("clientOrderId"))
        cum_qty = from_union([from_str, from_none], obj.get("cumQty"))
        cum_quote = from_union([from_str, from_none], obj.get("cumQuote"))
        executed_qty = from_union([from_str, from_none], obj.get("executedQty"))
        order_id = from_union([from_int, from_none], obj.get("orderId"))
        avg_price = from_union([from_str, from_none], obj.get("avgPrice"))
        orig_qty = from_union([from_str, from_none], obj.get("origQty"))
        price = from_union([from_str, from_none], obj.get("price"))
        reduce_only = from_union([from_bool, from_none], obj.get("reduceOnly"))
        side = from_union([from_str, from_none], obj.get("side"))
        position_side = from_union([from_str, from_none], obj.get("positionSide"))
        status = from_union([from_str, from_none], obj.get("status"))
        stop_price = from_union([from_str, from_none], obj.get("stopPrice"))
        close_position = from_union([from_bool, from_none], obj.get("closePosition"))
        symbol = from_union([from_str, from_none], obj.get("symbol"))
        time_in_force = from_union([from_str, from_none], obj.get("timeInForce"))
        order_type = from_union([from_str, from_none], obj.get("type"))
        orig_type = from_union([from_str, from_none], obj.get("origType"))
        activate_price = from_union([from_str, from_none], obj.get("activatePrice"))
        price_rate = from_union([from_str, from_none], obj.get("priceRate"))
        update_time = from_union([from_int, from_none], obj.get("updateTime"))
        working_type = from_union([from_str, from_none], obj.get("workingType"))
        price_protect = from_union([from_bool, from_none], obj.get("priceProtect"))
        return Order(client_order_id, cum_qty, cum_quote, executed_qty, order_id, avg_price, orig_qty, price,
                     reduce_only, side, position_side, status, stop_price, close_position, symbol, time_in_force,
                     order_type,
                     orig_type, activate_price, price_rate, update_time, working_type, price_protect)

    def to_dict(self) -> dict:
        result: dict = {}
        result["clientOrderId"] = from_union([from_str, from_none], self.client_order_id)
        result["cumQty"] = from_union([from_str, from_none], self.cum_qty)
        result["cumQuote"] = from_union([from_str, from_none], self.cum_quote)
        result["executedQty"] = from_union([from_str, from_none], self.executed_qty)
        result["orderId"] = from_union([from_int, from_none], self.order_id)
        result["avgPrice"] = from_union([from_str, from_none], self.avg_price)
        result["origQty"] = from_union([from_str, from_none], self.orig_qty)
        result["price"] = from_union([from_str, from_none], self.price)
        result["reduceOnly"] = from_union([from_bool, from_none], self.reduce_only)
        result["side"] = from_union([from_str, from_none], self.side)
        result["positionSide"] = from_union([from_str, from_none], self.position_side)
        result["status"] = from_union([from_str, from_none], self.status)
        result["stopPrice"] = from_union([from_str, from_none], self.stop_price)
        result["closePosition"] = from_union([from_bool, from_none], self.close_position)
        result["symbol"] = from_union([from_str, from_none], self.symbol)
        result["timeInForce"] = from_union([from_str, from_none], self.time_in_force)
        result["type"] = from_union([from_str, from_none], self.order_type)
        result["origType"] = from_union([from_str, from_none], self.orig_type)
        result["activatePrice"] = from_union([from_str, from_none], self.activate_price)
        result["priceRate"] = from_union([from_str, from_none], self.price_rate)
        result["updateTime"] = from_union([from_int, from_none], self.update_time)
        result["workingType"] = from_union([from_str, from_none], self.working_type)
        result["priceProtect"] = from_union([from_bool, from_none], self.price_protect)
        return result


def order_from_dict(s: Any) -> Order:
    return Order.from_dict(s)


def order_to_dict(x: Order) -> Any:
    return to_class(Order, x)
