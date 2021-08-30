import asyncio
import json
import time

from passivbot.passivbot import start_bot
from src.models.bot_config import BotConfig
from src.models.bot_user import UserBot
from src.services.logger import logger
from src.services.passivbot_binance import create_bot
# async def daemon_background_tasks():
#    schedule.every(30).minutes.do()
#    schedule.every(1).hour.do()
#    while True:
#        schedule.run_pending()
#        await asyncio.sleep(1)
from src.services.threadmanager.config import THREAD
from src.services.threadmanager.thread_manager import ThreadManager
from src.services.threadmanager.thread_statistics import enable_statistics


async def shutdown(signal, loop):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {signal.name}...")
    logger.info("Stopping all remaining tasks")
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]
    [task.cancel() for task in tasks]

    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def passivbot():
    print("llegaaa-main")

    # loop = asyncio.get_event_loop()
    # signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    # for s in signals:
    #    loop.add_signal_handler(
    #        s, lambda s=s: asyncio.create_task(shutdown(s, loop)))
    # try:
    #    loop.create_task(telegram.start_listener(on_expertmessage_message))
    #    loop.create_task(trading.start_trading())
    #    loop.create_task(daemon_background_tasks())
    #   loop.run_forever()
    # except KeyboardInterrupt:
    #    logger.info("Process interrupted")
    # finally:
    #    loop.close()
    #    logger.info("Successfully shutdown the Autotrading service.")

    def load_live_settings(exchange: str, user: str = 'default', do_print=True) -> BotConfig:
        settings = json.load(open(f'passivbot/configs/live/binance_manausdt.json'))
        if do_print:
            print('\nloaded settings:')
            print(json.dumps(settings, indent=4))
            settings_bot = BotConfig.from_dict(settings)
        return settings_bot

    settings = load_live_settings(exchange="Binance")
    symbol = "MANAUSDT"
    userbot = UserBot()
    userbot.id = 0
    userbot.name = "tests"
    userbot.key = "OGONpRKzRKMeFSnAk4DdbeCQz5nXflpb3mt6A1aooYbGC0j0H160zvCrPR4Zq2m5"
    userbot.secret = "qgxkE4nz4fLPDV8HZvrLwkdwJJ94FJ2Otfy2nRhIGVc12W3XhTN3XTHHbmUGSRwL"
    bot = create_bot(userbot, symbol, settings)
    await start_bot(bot)


def runpassivbot(loop):
    # asyncio.run_coroutine_threadsafe(passivbot(), loop)
    asyncio.run(passivbot())


def log_time(item: str):
    logger.debug(item)


def continuous_func(work_time: float):
    """A function that repeats until a stop is requested"""
    return_value: int = 0
    while tm.go:
        log_time("continuous_func - doing work")
        time.sleep(work_time)
        return_value += 1
    log_time("returning from continuous_func() as go is False")
    return return_value


if __name__ == '__main__':
    main_loop = asyncio.get_event_loop()
    # asyncio.run(main())
    enable_statistics()

    tm = ThreadManager("example", monitor_interval=1.0)
    tm.add_idle_callback(log_time, "went idle")
    tm.add_start_callback(log_time, "started")
    tm.add_stop_callback(log_time, "stopped")

    pool_name = "poolpassivbot"
    tm.add_pool(pool_name, THREAD, runtime_alert=1)
    # tm.add(pool_name, long_running_func, args=("first function", 1000), kwargs={"chunk_size": 20})
    threads = []
    thread_one = tm.add(pool_name, continuous_func, args=(.4,), get_ref=True, tag="test1")
    threads.append(thread_one)

    time.sleep(2)
    threads[0].cancel()
    threads.pop(0)
    time.sleep(2)
    thread_two = tm.add(pool_name, runpassivbot, args=(main_loop,), get_ref=True, tag="test2")
    threads.append(thread_one)

    # tm.stop()
    # tm.shutdown()

    # threading.Thread(target=flask_app.run).start()
