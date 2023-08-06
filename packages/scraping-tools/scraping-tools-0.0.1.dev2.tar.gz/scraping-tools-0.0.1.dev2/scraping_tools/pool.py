import contextlib
from multiprocessing import Pool

from scraping_tools.logger import logger


@contextlib.contextmanager
def safe_pool(process_number):
    """Process pool context manager.

    - Create a process pool with the given process number
    - Yields the pool
    - Quit & cleanup when done.

    :param num process_number: the required number of processes.
    """
    logger.debug("Starting a safe pool of %s processes", process_number)
    process_pool = Pool(processes=process_number)
    try:
        yield process_pool
    except:
        logger.exception("Pool encountered an unexpected error")
    finally:
        logger.debug("Cleaning up pool")
        process_pool.close()
        process_pool.join()
