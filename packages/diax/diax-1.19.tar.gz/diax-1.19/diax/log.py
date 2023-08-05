import logging

def setup(level=logging.INFO):
    logging.basicConfig(level=level, format="[%(asctime)s] %(levelname)s pid:%(process)d %(name)s:%(lineno)d %(message)s")
