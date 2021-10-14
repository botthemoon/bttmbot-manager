from src.services.dockermanager import create_passivbot_image, run_bot_container, is_image_created


def run_passivbot(market_type: str, symbol: str, userbot_name: str, userbot_key: str, userbot_secret: str):
    env_bot = {}
    env_bot["PASSIVBOT_MARKET_TYPE"] = market_type
    env_bot["PASSIVBOT_SYMBOL"] = symbol.upper()
    env_bot["PASSIVBOT_CONFIG_PATH"] = f'passivbot/configs/live/binance_{symbol.lower()}.json'
    env_bot["PASSIVBOT_BINANCE_KEY"] = userbot_key
    env_bot["PASSIVBOT_BINANCE_SECRET"] = userbot_secret
    return run_bot_container(env=env_bot, name=userbot_name)


if __name__ == '__main__':
    if not is_image_created():
        create_passivbot_image()
