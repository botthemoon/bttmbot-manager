from bttmbotmanager.services.dockermanager import (
    run_bot_container,
    is_image_created,
    create_bttmbot_image,
)


def run_bttmbot(
    market_type: str,
    symbol: str,
    userbot_name: str,
    userbot_key: str,
    userbot_secret: str,
):
    env_bot = {}
    env_bot["BTTMBOT_MARKET_TYPE"] = market_type
    env_bot["BTTMBOT_SYMBOL"] = symbol.upper()
    # env_bot["BTTMBOT_CONFIG_PATH"] = f"bttmbot/configs/live/binance_{symbol.lower()}.json"
    env_bot["BTTMBOT_CONFIG_PATH"] = "bttmbot/configs/live/multi_122_symbols.json"
    env_bot["BTTMBOT_BINANCE_KEY"] = userbot_key
    env_bot["BTTMBOT_BINANCE_SECRET"] = userbot_secret
    return run_bot_container(env=env_bot, name=userbot_name)


if __name__ == "__main__":
    if not is_image_created():
        create_bttmbot_image()
