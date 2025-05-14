import asyncio
import sys

from database import db
from dispatcher import bot, dp
from handlers import error_handling, client_handlers
from logger import logger


async def main() -> None:
    # Initializing the database
    try:
        await db.create_pool()

    except BaseException as e:
        logger.critical("DATA BASE IS NOT CONNECTED, SO PROCESS WILL BE STOPPED!")
        raise e

    else:
        logger.info("DATA BASE IS SUCCESSFUL CONNECTED!")

    # Skipping all accumulated updates
    await bot.delete_webhook(drop_pending_updates=True)

    # Connecting routers to the dispatcher
    dp.include_routers(error_handling.router)
    dp.include_router(client_handlers.router)

    logger.info("ALL ROUTERS ARE CONNECTED!")

    # Run events dispatching
    logger.info("BOT IS STARTED!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.critical("BOT IS STOPPED!")
        sys.exit()

    except BaseException as ex:
        logger.critical(f"BOT IS STOPPED! ERROR: {ex}")
        raise ex
