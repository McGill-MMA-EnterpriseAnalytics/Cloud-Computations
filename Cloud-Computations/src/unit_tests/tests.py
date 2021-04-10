import logging


def working():
    logger = logging.getLogger(__name__)
    logger.info('Working')
    #print("Working")

def main():
    working()

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()