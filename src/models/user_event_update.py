from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any, TypeVar, Type, cast, List, Callable

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
            logger.debug("User event order assert exception: " + str(fs) + str(x))
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class OrderTradeEvent:
    class Side(str, Enum):
        BUY = 'BUY'
        SELL = 'SELL'

        @staticmethod
        def from_str(side):
            if side in 'BUY':
                return OrderTradeEvent.Side.BUY
            elif side in 'SELL':
                return OrderTradeEvent.Side.SELL
            else:
                raise NotImplementedError

    class OrderType(str, Enum):
        MARKET = 'MARKET'
        LIMIT = 'LIMIT'
        STOP = 'STOP'
        TAKE_PROFIT = 'TAKE_PROFIT'
        LIQUIDATION = 'LIQUIDATION'

        @staticmethod
        def from_str(order_type):
            if order_type in 'MARKET':
                return OrderTradeEvent.OrderType.MARKET
            elif order_type in 'LIMIT':
                return OrderTradeEvent.OrderType.LIMIT
            elif order_type in 'STOP':
                return OrderTradeEvent.OrderType.STOP
            elif order_type in 'TAKE_PROFIT':
                return OrderTradeEvent.OrderType.TAKE_PROFIT
            elif order_type in 'LIQUIDATION':
                return OrderTradeEvent.OrderType.LIQUIDATION
            else:
                raise NotImplementedError

    class ExecutionType(str, Enum):
        NEW = 'NEW'
        CANCELED = 'CANCELED'
        CALCULATED = 'CALCULATED'
        EXPIRED = 'EXPIRED'
        TRADE = 'TRADE'

        @staticmethod
        def from_str(execution_type):
            if execution_type in 'NEW':
                return OrderTradeEvent.ExecutionType.NEW
            elif execution_type in 'CANCELED':
                return OrderTradeEvent.ExecutionType.CANCELED
            elif execution_type in 'CALCULATED':
                return OrderTradeEvent.ExecutionType.CALCULATED
            elif execution_type in 'EXPIRED':
                return OrderTradeEvent.ExecutionType.EXPIRED
            elif execution_type in 'TRADE':
                return OrderTradeEvent.ExecutionType.TRADE
            else:
                raise NotImplementedError

    class OrderStatus(str, Enum):
        NEW = 'NEW'
        PARTIALLY_FILLED = 'PARTIALLY_FILLED'
        FILLED = 'FILLED'
        CANCELED = 'CANCELED'
        EXPIRED = 'EXPIRED'
        NEW_INSURANCE = 'NEW_INSURANCE'
        NEW_ADL = 'NEW_ADL'

        @staticmethod
        def from_str(status):
            if status in 'NEW':
                return OrderTradeEvent.OrderStatus.NEW
            elif status in 'PARTIALLY_FILLED':
                return OrderTradeEvent.OrderStatus.PARTIALLY_FILLED
            elif status in 'FILLED':
                return OrderTradeEvent.OrderStatus.FILLED
            elif status in 'CANCELED':
                return OrderTradeEvent.OrderStatus.CANCELED
            elif status in 'EXPIRED':
                return OrderTradeEvent.OrderStatus.EXPIRED
            elif status in 'NEW_INSURANCE':
                return OrderTradeEvent.OrderStatus.NEW_INSURANCE
            elif status in 'NEW_ADL':
                return OrderTradeEvent.OrderStatus.NEW_ADL
            else:
                raise NotImplementedError

    class TimeInForce(str, Enum):
        GTC = 'GTC'  # Good till cancelled
        IOC = 'IOC'  # Immediate or cancel
        FOK = 'FOK'  # Fill or kill
        GTX = 'GTX'

        @staticmethod
        def from_str(time_in_force_type):
            if time_in_force_type in 'GTC':
                return OrderTradeEvent.TimeInForce.GTC
            elif time_in_force_type in 'IOC':
                return OrderTradeEvent.TimeInForce.IOC
            elif time_in_force_type in 'FOK':
                return OrderTradeEvent.TimeInForce.FOK
            elif time_in_force_type in 'GTX':
                return OrderTradeEvent.TimeInForce.GTX
            else:
                raise NotImplementedError

    class WorkingType(str, Enum):
        MARK_PRICE = 'MARK_PRICE'
        CONTRACT_PRICE = 'CONTRACT_PRICE'

        @staticmethod
        def from_str(side):
            if side in 'MARK_PRICE':
                return OrderTradeEvent.WorkingType.MARK_PRICE
            elif side in 'CONTRACT_PRICE':
                return OrderTradeEvent.WorkingType.CONTRACT_PRICE
            else:
                raise NotImplementedError

    original_price: Optional[str] = None
    avereage_price: Optional[str] = None
    order_last: Optional[str] = None
    order_filled: Optional[str] = None
    last_filled: Optional[str] = None
    comission: Optional[str] = None
    bids_notional: Optional[str] = None
    realized_profit: Optional[str] = None
    order_symbol: Optional[str] = None
    client_order_id: Optional[str] = None
    side: Optional[Side] = None
    order_type: Optional[OrderType] = None
    time_in_force: Optional[TimeInForce] = None
    original_quantity: Optional[str] = None
    stop_price: Optional[str] = None
    execution_type: Optional[ExecutionType] = None
    order_status: Optional[OrderStatus] = None
    order_id: Optional[int] = None
    comission_asset: Optional[str] = None
    order_trade: Optional[int] = None
    trade_id: Optional[int] = None
    ask_notional: Optional[str] = None
    trade_maker_side: Optional[bool] = None
    reduce_only: Optional[bool] = None
    stop_price_working_type: Optional[WorkingType] = None
    original_order_type: Optional[str] = None
    position_side: Optional[str] = None
    close_position: Optional[bool] = None
    activation_price: Optional[str] = None
    callback_rate: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'OrderTradeEvent':
        assert isinstance(obj, dict)
        original_price = from_union([from_str, from_none], obj.get("p"))
        avereage_price = from_union([from_str, from_none], obj.get("ap"))
        order_last = from_union([from_str, from_none], obj.get("l"))
        order_filled = from_union([from_str, from_none], obj.get("z"))
        last_filled = from_union([from_str, from_none], obj.get("L"))
        comission = from_union([from_str, from_none], obj.get("n"))
        bids_notional = from_union([from_str, from_none], obj.get("b"))
        realized_profit = from_union([from_str, from_none], obj.get("rp"))
        order_symbol = from_union([from_str, from_none], obj.get("s"))
        client_order_id = from_union([from_str, from_none], obj.get("c"))
        side = from_union([OrderTradeEvent.Side.from_str, from_none], obj.get("S"))
        order_type = from_union([OrderTradeEvent.OrderType.from_str, from_none], obj.get("o"))
        time_in_force = from_union([OrderTradeEvent.TimeInForce.from_str, from_none], obj.get("f"))
        original_quantity = from_union([from_str, from_none], obj.get("q"))
        stop_price = from_union([from_str, from_none], obj.get("sp"))
        execution_type = from_union([OrderTradeEvent.ExecutionType.from_str, from_none], obj.get("x"))
        order_status = from_union([OrderTradeEvent.OrderStatus.from_str, from_none], obj.get("X"))
        order_id = from_union([from_int, from_none], obj.get("i"))
        comission_asset = from_union([from_str, from_none], obj.get("N"))
        order_trade = from_union([from_int, from_none], obj.get("T"))
        trade_id = from_union([from_int, from_none], obj.get("t"))
        ask_notional = from_union([from_str, from_none], obj.get("a"))
        trade_maker_side = from_union([from_bool, from_none], obj.get("m"))
        reduce_only = from_union([from_bool, from_none], obj.get("R"))
        stop_price_working_type = from_union([OrderTradeEvent.WorkingType.from_str, from_none], obj.get("wt"))
        original_order_type = from_union([from_str, from_none], obj.get("ot"))
        position_side = from_union([from_str, from_none], obj.get("ps"))
        close_position = from_union([from_bool, from_none], obj.get("cp"))
        activation_price = from_union([from_str, from_none], obj.get("AP"))
        callback_rate = from_union([from_str, from_none], obj.get("cr"))
        return OrderTradeEvent(original_price, avereage_price, order_last, order_filled, last_filled, comission,
                               bids_notional, realized_profit, order_symbol, client_order_id, side, order_type,
                               time_in_force, original_quantity, stop_price,
                               execution_type, order_status, order_id, comission_asset, order_trade, trade_id,
                               ask_notional,
                               trade_maker_side, reduce_only, stop_price_working_type, original_order_type,
                               position_side,
                               close_position,
                               activation_price, callback_rate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["p"] = from_union([from_str, from_none], self.original_price)
        result["ap"] = from_union([from_str, from_none], self.avereage_price)
        result["l"] = from_union([from_str, from_none], self.order_last)
        result["z"] = from_union([from_str, from_none], self.order_filled)
        result["L"] = from_union([from_str, from_none], self.last_filled)
        result["n"] = from_union([from_str, from_none], self.comission)
        result["b"] = from_union([from_str, from_none], self.bids_notional)
        result["rp"] = from_union([from_str, from_none], self.realized_profit)
        result["s"] = from_union([from_str, from_none], self.order_symbol)
        result["c"] = from_union([from_str, from_none], self.client_order_id)
        result["S"] = from_union([OrderTradeEvent.Side.from_str, from_none], self.side)
        result["o"] = from_union([OrderTradeEvent.OrderType.from_str, from_none], self.order_type)
        result["f"] = from_union([OrderTradeEvent.TimeInForce.from_str, from_none], self.time_in_force)
        result["q"] = from_union([from_str, from_none], self.original_quantity)
        result["sp"] = from_union([from_str, from_none], self.stop_price)
        result["x"] = from_union([OrderTradeEvent.ExecutionType.from_str, from_none], self.execution_type)
        result["X"] = from_union([OrderTradeEvent.OrderStatus.from_str, from_none], self.order_status)
        result["i"] = from_union([from_int, from_none], self.order_id)
        result["N"] = from_union([from_str, from_none], self.comission_asset)
        result["T"] = from_union([from_int, from_none], self.order_trade)
        result["t"] = from_union([from_int, from_none], self.trade_id)
        result["a"] = from_union([from_str, from_none], self.ask_notional)
        result["m"] = from_union([from_bool, from_none], self.trade_maker_side)
        result["R"] = from_union([from_bool, from_none], self.reduce_only)
        result["wt"] = from_union([OrderTradeEvent.WorkingType.from_str, from_none], self.stop_price_working_type)
        result["ot"] = from_union([from_str, from_none], self.original_order_type)
        result["ps"] = from_union([from_str, from_none], self.position_side)
        result["cp"] = from_union([from_bool, from_none], self.close_position)
        result["AP"] = from_union([from_str, from_none], self.activation_price)
        result["cr"] = from_union([from_str, from_none], self.callback_rate)
        return result


@dataclass
class AccountConfigEvent:
    symbol: Optional[str] = None
    leverage: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AccountConfigEvent':
        assert isinstance(obj, dict)
        symbol = from_union([from_str, from_none], obj.get("s"))
        leverage = from_union([from_int, from_none], obj.get("l"))
        return AccountConfigEvent(symbol, leverage)

    def to_dict(self) -> dict:
        result: dict = {}
        result["s"] = from_union([from_str, from_none], self.symbol)
        result["l"] = from_union([from_int, from_none], self.leverage)
        return result


@dataclass
class AccountUpdateEvent:
    class EventReasonType(str, Enum):
        DEPOSIT = 'DEPOSIT'
        WITHDRAW = 'WITHDRAW'
        ORDER = 'ORDER'
        FUNDING_FEE = 'FUNDING_FEE'
        WITHDRAW_REJECT = 'WITHDRAW_REJECT'
        ADJUSTMENT = 'ADJUSTMENT'
        INSURANCE_CLEAR = 'INSURANCE_CLEAR'
        ADMIN_DEPOSIT = 'ADMIN_DEPOSIT'
        ADMIN_WITHDRAW = 'ADMIN_WITHDRAW'
        MARGIN_TRANSFER = 'MARGIN_TRANSFER'
        MARGIN_TYPE_CHANGE = 'MARGIN_TYPE_CHANGE'
        ASSET_TRANSFER = 'ASSET_TRANSFER'
        OPTIONS_PREMIUM_FEE = 'OPTIONS_PREMIUM_FEE'
        OPTIONS_SETTLE_PROFIT = 'OPTIONS_SETTLE_PROFIT'

        @staticmethod
        def from_str(reason_type):
            if reason_type in 'DEPOSIT':
                return AccountUpdateEvent.EventReasonType.DEPOSIT
            elif reason_type in 'WITHDRAW':
                return AccountUpdateEvent.EventReasonType.WITHDRAW
            elif reason_type in 'ORDER':
                return AccountUpdateEvent.EventReasonType.ORDER
            elif reason_type in 'FUNDING_FEE':
                return AccountUpdateEvent.EventReasonType.FUNDING_FEE
            elif reason_type in 'WITHDRAW_REJECT':
                return AccountUpdateEvent.EventReasonType.WITHDRAW_REJECT
            elif reason_type in 'INSURANCE_CLEAR':
                return AccountUpdateEvent.EventReasonType.INSURANCE_CLEAR
            elif reason_type in 'ADMIN_DEPOSIT':
                return AccountUpdateEvent.EventReasonType.ADMIN_DEPOSIT
            elif reason_type in 'ADMIN_WITHDRAW':
                return AccountUpdateEvent.EventReasonType.ADMIN_WITHDRAW
            elif reason_type in 'MARGIN_TRANSFER':
                return AccountUpdateEvent.EventReasonType.MARGIN_TRANSFER
            elif reason_type in 'MARGIN_TYPE_CHANGE':
                return AccountUpdateEvent.EventReasonType.MARGIN_TYPE_CHANGE
            elif reason_type in 'ASSET_TRANSFER':
                return AccountUpdateEvent.EventReasonType.ASSET_TRANSFER
            elif reason_type in 'OPTIONS_PREMIUM_FEE':
                return AccountUpdateEvent.EventReasonType.OPTIONS_PREMIUM_FEE
            elif reason_type in 'OPTIONS_SETTLE_PROFIT':
                return AccountUpdateEvent.EventReasonType.OPTIONS_SETTLE_PROFIT
            else:
                raise NotImplementedError

    @dataclass
    class Balance:
        asset: Optional[str] = None
        wallet_balance: Optional[str] = None
        cross_wallet_balance: Optional[str] = None

        @staticmethod
        def from_dict(obj: Any) -> 'Balance':
            assert isinstance(obj, dict)
            asset = from_union([from_str, from_none], obj.get("a"))
            wallet_balance = from_union([from_str, from_none], obj.get("wb"))
            cross_wallet_balance = from_union([from_str, from_none], obj.get("cw"))
            return AccountUpdateEvent.Balance(asset, wallet_balance, cross_wallet_balance)

        def to_dict(self) -> dict:
            result: dict = {}
            result["a"] = from_union([from_str, from_none], self.asset)
            result["wb"] = from_union([from_str, from_none], self.wallet_balance)
            result["cw"] = from_union([from_str, from_none], self.cross_wallet_balance)
            return result

    @dataclass
    class Position:
        symbol: Optional[str] = None
        position_amount: Optional[str] = None
        entry_price: Optional[str] = None
        accumulated_realized: Optional[str] = None
        unrealized_pnl: Optional[str] = None
        margin_type: Optional[str] = None
        isolated_wallet: Optional[str] = None
        position_side: Optional[str] = None

        @staticmethod
        def from_dict(obj: Any) -> 'Position':
            assert isinstance(obj, dict)
            symbol = from_union([from_str, from_none], obj.get("s"))
            position_amount = from_union([from_str, from_none], obj.get("pa"))
            entry_price = from_union([from_str, from_none], obj.get("ep"))
            accumulated_realized = from_union([from_str, from_none], obj.get("cr"))
            unrealized_pnl = from_union([from_str, from_none], obj.get("up"))
            margin_type = from_union([from_str, from_none], obj.get("mt"))
            isolated_wallet = from_union([from_str, from_none], obj.get("iw"))
            position_side = from_union([from_str, from_none], obj.get("ps"))
            return AccountUpdateEvent.Position(symbol, position_amount, entry_price, accumulated_realized,
                                               unrealized_pnl, margin_type, isolated_wallet, ps)

        def to_dict(self) -> dict:
            result: dict = {}
            result["s"] = from_union([from_str, from_none], self.symbol)
            result["pa"] = from_union([from_str, from_none], self.position_amount)
            result["ep"] = from_union([from_str, from_none], self.entry_price)
            result["cr"] = from_union([from_str, from_none], self.accumulated_realized)
            result["up"] = from_union([from_str, from_none], self.unrealized_pnl)
            result["mt"] = from_union([from_str, from_none], self.margin_type)
            result["iw"] = from_union([from_str, from_none], self.isolated_wallet)
            result["ps"] = from_union([from_str, from_none], self.position_side)
            return result

    event_reason_type: Optional[EventReasonType] = None
    balance: Optional[List[Balance]] = None
    position: Optional[List[Position]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AccountUpdateEvent':
        assert isinstance(obj, dict)
        event_reason_type = from_union([AccountUpdateEvent.EventReasonType.from_str, from_none], obj.get("m"))
        balance = from_union([lambda x: from_list(AccountUpdateEvent.Balance.from_dict, x), from_none],
                             obj.get("Balance"))
        position = from_union([lambda x: from_list(AccountUpdateEvent.Position.from_dict, x), from_none],
                              obj.get("Position"))
        return AccountUpdateEvent(event_reason_type, balance, position)

    def to_dict(self) -> dict:
        result: dict = {}
        result["m"] = from_union([AccountUpdateEvent.EventReasonType.from_str, from_none], self.event_reason_type)
        result["Balance"] = from_union(
            [lambda x: from_list(lambda x: to_class(AccountUpdateEvent.Balance, x), x), from_none],
            self.balance)
        result["Position"] = from_union(
            [lambda x: from_list(lambda x: to_class(AccountUpdateEvent.Position, x), x), from_none],
            self.position)
        return result


@dataclass
class UserEventUpdate:
    class EventType(str, Enum):
        ACCOUNT_CONFIG_UPDATE = 'ACCOUNT_CONFIG_UPDATE'
        ACCOUNT_UPDATE = 'ACCOUNT_UPDATE'
        ORDER_TRADE_UPDATE = 'ORDER_TRADE_UPDATE'

        @staticmethod
        def from_str(event_type):
            if event_type in 'ACCOUNT_CONFIG_UPDATE':
                return UserEventUpdate.EventType.ACCOUNT_CONFIG_UPDATE
            elif event_type in 'ACCOUNT_UPDATE':
                return UserEventUpdate.EventType.ACCOUNT_UPDATE
            elif event_type in 'ORDER_TRADE_UPDATE':
                return UserEventUpdate.EventType.ORDER_TRADE_UPDATE
            else:
                raise NotImplementedError

    event_type: Optional[EventType] = None
    event_time: Optional[int] = None
    transaction_time: Optional[int] = None
    order_trade: Optional[OrderTradeEvent] = None
    account_config: Optional[AccountConfigEvent] = None
    account_update: Optional[AccountUpdateEvent] = None

    @staticmethod
    def from_dict(obj: Any) -> 'UserEventUpdate':
        assert isinstance(obj, dict)
        event_type = from_union([UserEventUpdate.EventType.from_str, from_none], obj.get("e"))
        event_time = from_union([from_int, from_none], obj.get("E"))
        transaction_time = from_union([from_int, from_none], obj.get("T"))
        order = from_union([OrderTradeEvent.from_dict, from_none], obj.get("o"))
        account_config = from_union([AccountConfigEvent.from_dict, from_none], obj.get("ac"))
        account_update = from_union([AccountUpdateEvent.from_dict, from_none], obj.get("a"))
        return UserEventUpdate(event_type, event_time, transaction_time, order, account_config, account_update)

    def to_dict(self) -> dict:
        result: dict = {}
        result["e"] = from_union([UserEventUpdate.EventType.from_str, from_none], self.event_type)
        result["E"] = from_union([from_int, from_none], self.event_time)
        result["T"] = from_union([from_int, from_none], self.transaction_time)
        result["o"] = from_union([lambda x: to_class(OrderTradeEvent, x), from_none], self.order_trade)
        result["ac"] = from_union([lambda x: to_class(AccountConfigEvent, x), from_none], self.account_config)
        result["a"] = from_union([lambda x: to_class(AccountUpdateEvent, x), from_none], self.account_update)
        return result


def user_event_update_from_dict(s: Any) -> UserEventUpdate:
    return UserEventUpdate.from_dict(s)


def user_event_update_to_dict(x: UserEventUpdate) -> Any:
    return to_class(UserEventUpdate, x)
