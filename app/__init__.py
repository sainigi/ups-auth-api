from dotenv import load_dotenv
import logging.config

load_dotenv()
formatter = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"
logging.basicConfig(format=formatter, level=logging.DEBUG)

loggers = ['urllib3', 'asyncio', 'uamqp', 'azure', 'msal']

for logger in loggers:
    ll = logging.getLogger(logger)
    ll.setLevel(logging.CRITICAL)
