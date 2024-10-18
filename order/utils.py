import requests as re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# TODO: Retry Mechanism
def buy_from_exchange(token_name, quantity):
    logging.info(f"calling the external API to buy {quantity} of {token_name}.")
    url = 'https://api.beederang.com/faq/'
    result = re.get(url=url)
    return result
