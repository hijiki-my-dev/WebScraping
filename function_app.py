import time

import azure.functions as func

from src.job import run
from src.modules import delete_old_pages
from src.utils import Logger, log_level

logger = Logger(log_level=log_level)


app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 0 1 * * 6", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def ScrapingJob(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logger.error("The timer is past due!")

    delete_old_pages()
    time.sleep(3)
    run()
    logger.info("Python timer trigger function executed.")
