import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from app.actors.clear_expired_authorizations import clear_expired_authorizations

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    scheduler = BlockingScheduler()
    scheduler.add_job(
        clear_expired_authorizations,
        # Every 5 minutes
        CronTrigger.from_crontab("*/5 * * * *"),
    )

    try:
        logging.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logging.info("Shutting down scheduler...")
        scheduler.shutdown()
