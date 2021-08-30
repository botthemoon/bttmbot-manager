from pathlib import Path

import aiohttp as aiohttp
import numpy as np

from passivbot.binance import BinanceBot
from passivbot.passivbot import make_get_filepath
from src.models.bot_config import BotConfig
from src.models.bot_user import UserBot


async def create_bot(user: UserBot, symbol: str, settings: BotConfig):
    bot = PassivbotBinance(user, symbol, settings)
    await bot._init()
    return bot


class PassivbotBinance(BinanceBot):
    def __init__(self, user: UserBot, symbol: str, settings: BotConfig):
        self.exchange = 'binance'
        self.symbol = symbol
        self.max_pos_size_ito_usdt = 0.0
        self.max_pos_size_ito_coin = 0.0
        self.session = aiohttp.ClientSession()
        self.base_endpoint = ''
        self.key = user.key
        self.secret = user.secret
        self.config = settings.to_dict()

        self.config['do_long'] = self.config['long']['enabled']
        self.config['do_shrt'] = self.config['shrt']['enabled']
        self.config['max_leverage'] = 25
        self.telegram = None
        self.xk = {}

        self.hedge_mode = self.config['hedge_mode'] = True
        self.set_config(self.config)

        self.ema_alpha = 2.0 / (self.spans + 1.0)
        self.ema_alpha_ = 1.0 - self.ema_alpha

        self.ts_locked = {'cancel_orders': 0.0, 'decide': 0.0, 'update_open_orders': 0.0,
                          'update_position': 0.0, 'print': 0.0, 'create_orders': 0.0,
                          'check_fills': 0.0}
        self.ts_released = {k: 1.0 for k in self.ts_locked}

        self.position = {}
        self.open_orders = []
        self.fills = []
        self.highest_bid = 0.0
        self.lowest_ask = 9.9e9
        self.price = 0
        self.is_buyer_maker = True
        self.agg_qty = 0.0
        self.qty = 0.0
        self.ob = [0.0, 0.0]

        self.emas = np.zeros(len(self.spans))
        self.ratios = np.zeros(len(self.spans))

        self.n_open_orders_limit = 8
        self.n_orders_per_execution = 4

        self.c_mult = self.config['c_mult'] = 1.0

        self.log_filepath = make_get_filepath(f"logs/{self.exchange}/{self.config['config_name']}.log")

        self.log_level = 0

        self.stop_websocket = False
        self.process_websocket_ticks = True
        self.lock_file = f"{str(Path.home())}/.{self.exchange}_passivbotlock"
