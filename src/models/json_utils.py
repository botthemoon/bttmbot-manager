import dataclasses
import json

from src.models.order import Order
from src.models.user_event_update import OrderTradeEvent, AccountConfigEvent, AccountUpdateEvent


class EnhancedJSONDecoder(json.JSONDecoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, Order):
            return {'order': o.from_dict()}
        elif isinstance(o, OrderTradeEvent):
            return {'order_event': o.from_dict()}
        elif isinstance(o, AccountConfigEvent):
            return {'account_config': o.from_dict()}
        elif isinstance(o, AccountUpdateEvent):
            return {'account_update': o.from_dict()}
        else:
            return json.JSONDecoder.default(self, o)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, Order):
            return {'order': o.to_dict()}
        elif isinstance(o, OrderTradeEvent):
            return {'order_event': o.to_dict()}
        elif isinstance(o, AccountConfigEvent):
            return {'account_config': o.to_dict()}
        elif isinstance(o, AccountUpdateEvent):
            return {'account_update': o.to_dict()}
        else:
            return json.JSONEncoder.default(self, o)
